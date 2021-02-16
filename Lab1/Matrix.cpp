#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <sstream>
#include <cmath>
#include "Matrix.h"

#define eps 1e-9

Matrix::Matrix() : rows_(1), cols_(1)
{
    allocate();
    el[0][0] = 0;
}

Matrix::Matrix(int rows, int cols) : rows_(rows), cols_(cols)
{
    allocate();
    for(int i = 0; i < rows_; i++){
        for(int j = 0 ; j < cols_; j++){
            el[i][j] = 0;
        }
    }
}

Matrix::Matrix(const Matrix &matrix) : rows_(matrix.rows_), cols_(matrix.cols_)
{
    allocate();
    for(int i = 0; i < rows_; i++){
        for(int j = 0; j < cols_; j++){
            el[i][j] = matrix.el[i][j];
        }
    }
}

Matrix::Matrix(const char *filename)
{
    std::ifstream stream(filename);
    std::string str;
    std::vector<std::vector<std::string>> m;
    std::vector<std::string> result;
    int c = 0, r = 0;

    while(std::getline(stream, str)) {
        std::istringstream iss(str);
        for(std::string s; iss >> s;){
            result.push_back(s);
        }
        m.push_back(result);
        if(r == 0) {
            c = result.size();
        }
        result.clear();
        r++;
    }
    stream.close();
    rows_ = r;
    cols_ = c;
    allocate();
    int i = 0, j = 0;
    for(auto row : m){
        for(auto elem : row){
            el[i][j] = (double)atof(elem.c_str());
            j++;
        }
        i++;
        j = 0;
    }
}

Matrix::~Matrix() {
    for(int i = 0; i < rows_; i++){
        delete[] el[i];
    }
    delete[] el;
}

std::ostream& operator<<(std::ostream &ostream, const Matrix &matrix)
{
    for(int i = 0; i < matrix.rows_; i++){
        for(int j = 0; j < matrix.cols_; j++){
            ostream << "\t" << matrix.el[i][j];
        }
        ostream << "\n";
    }
    return ostream;
}

void Matrix::output(const char *filename)
{
    std::ofstream stream(filename);
    std::string str;

    if(stream.is_open()){
        for(int i = 0; i < rows_; i++){
            for(int j = 0; j < cols_; j++){
                stream << el[i][j] << " ";
            }
            stream << "\n";
        }
        stream.close();
    } else {
        std::cout << "Unable to open the file!\n";
    }

}

double& Matrix::operator()(int x, int y)
{
    return el[x][y];
}

double *&Matrix::operator[](const int x) {
    return el[x];
}

// Operator pridruživanja
Matrix& Matrix::operator=(const Matrix &matrix)
{
    if(this == &matrix){
        return *this;
    }

    if(rows_ != matrix.rows_ || cols_ != matrix.cols_){
        for(int i = 0; i < rows_; i++){
            delete[] el[i];
        }
        delete[] el;

        rows_ = matrix.rows_;
        cols_ = matrix.cols_;
        allocate();
    }

    for(int i = 0; i < rows_; i++){
        for(int j = 0; j < cols_; j++){
            el[i][j] = matrix.el[i][j];
        }
    };
    return *this;
}

Matrix& Matrix::operator+=(const Matrix &matrix)
{
    for(int i = 0; i < rows_; i++){
        for(int j = 0; j < cols_; j++){
            el[i][j] += matrix.el[i][j];
        }
    }
    return *this;
}

Matrix& Matrix::operator-=(const Matrix &matrix)
{
    for(int i = 0; i < rows_; i++){
        for(int j = 0; j < cols_; j++){
            el[i][j] -= matrix.el[i][j];
        }
    }
    return *this;
}

Matrix& Matrix::operator*=(double value)
{
    for(int i = 0; i < rows_; i++){
        for(int j = 0; j < cols_; j++){
            el[i][j] *= value;
            if(fabs(el[i][j]) < eps) el[i][j] = 0;
        }
    }
    return *this;
}

Matrix& Matrix::operator*=(const Matrix &matrix)
{
    if(cols_ != matrix.rows_) {
        std::cout << "Matrice nisu ulancane! Nema umnoska!\n";
    }
    Matrix product(rows_, matrix.cols_);
    for(int i = 0; i < product.rows_; i++){
        for(int j = 0; j < product.cols_; j++){
            for(int k = 0; k < cols_; k++){
                product.el[i][j] += (el[i][k] * matrix.el[k][j]);
                if(fabs(product.el[i][j]) < eps) product.el[i][j] = 0;
            }
        }
    }
    *this = product;
    return *this;
}

bool Matrix::operator==(const Matrix &matrix)
{
    if(rows_ != matrix.rows_ || cols_ != matrix.cols_){
        return false;
    }

    for(int i = 0; i < rows_; i++){
        for(int j = 0; j < cols_; j++){
            if(el[i][j] != matrix.el[i][j]) return false;
        }
    }

    return true;
}

Matrix Matrix::transpose()
{
    Matrix matrix(cols_, rows_);
    for(int i = 0; i < cols_; i++){
        for(int j = 0; j < rows_; j++){
            matrix.el[i][j] = el[j][i];
        }
    }
    return matrix;
}

void Matrix::swapRows(int x, int y)
{
    double *t = el[x];
    el[x] = el[y];
    el[y] = t;
}

void Matrix::LU()
{
    int n = rows_;
    for(int i = 0; i < n; i++){
        for(int j = i + 1; j < n; j++){
            if(fabs(el[i][i]) < eps && i != n - 1) {
                std::cout << "Pivot element " << el[i][i] << " je (priblizno) 0! LU dekompozicija nije moguca.\n";
                return;
            }
            el[j][i] /= el[i][i];
            for(int k = i + 1; k  < n; k++){
                el[j][k] -= el[j][i] * el[i][k];
            }
        }
    }
}

Matrix Matrix::LUP()
{
    int n = rows_;
    Matrix P(n, 1);
    Matrix R(n, 1);
    for(int i = 0; i < n; i++){
        P[i][0] = i;
        R[i][0] = i;
    }
    for(int i = 0; i < n - 1; i++){
        int pivot = i;
        for(int j = i + 1; j < n; j++){
            if(fabs(el[(int)P[j][0]][i]) > fabs(el[(int)P[pivot][0]][i])){
                pivot = j;
            }
        }
        swapRows((int)P[i][0],(int)P[pivot][0]);
        R.swapRows((int)P[i][0],(int)P[pivot][0]);
        if(fabs(el[(int)P[i][0]][i]) < eps) {
            std::cout << "Pivot element je (priblizno) 0!\n";
            return nullptr;
        }
        for(int j = i + 1; j < n; j++){
            el[(int)P[j][0]][i] /= el[(int)P[i][0]][i];
            for(int k = i + 1; k < n; k++){
                el[(int)P[j][0]][k] -= el[(int)P[j][0]][i] * el[i][(int)P[k][0]];
                if(fabs(el[(int)P[j][0]][k]) < eps) el[(int)P[j][0]][k] = 0;
            }
        }
    }
    return R;
}

Matrix Matrix::forwardSubstitution(Matrix L, Matrix b)
{
    int n = b.rows_;
    Matrix y = b;
    for(int i = 0; i < n - 1; i++){
        for(int j = i + 1; j < n; j++){
            y[j][0] -= L[j][i] * y[i][0];
            if(fabs(y[j][0]) < eps) y[j][0] = 0;
        }
    }
    return y;
}

Matrix Matrix::backSubstitution(Matrix U, Matrix y)
{
    int n = y.rows_;
    Matrix x = y;
    for(int i = n - 1; i >= 0; i--){
        if(fabs(U[i][i]) < eps){
            std::cout << "Sustav nema rjesenje.\n";
            return nullptr;
        }
        x[i][0] /= U[i][i];
        for(int j = 0; j <= i - 1; j++){
            x[j][0] -= U[j][i] * x[i][0];
            if(fabs(x[j][0]) < eps) x[j][0] = 0;
        }
    }
    return x;
}

Matrix Matrix::permutationMatrix()
{
    if(cols_ != 1) {
        std::cout << "Ulaz treba biti vektor!\n";
        return nullptr;
    }
    int n = rows_;
    Matrix P(n, n);
    for(int i = 0; i < n; i++){
        P[i][(int)el[i][0]] = 1;
    }
    return P;
}

Matrix Matrix::inverse(Matrix matrix)
{
    Matrix inv(matrix.rows_, matrix.cols_);
    Matrix P = matrix.LUP().permutationMatrix();
    Matrix E = Matrix::identity(matrix.rows_);
    Matrix X(matrix.rows_, matrix.cols_);
    for(int i = 0; i < matrix.rows_; i++){
        Matrix ei(1, matrix.cols_);
        ei[0][i] = 1;
        Matrix yi = Matrix::forwardSubstitution(matrix, P * ei.transpose());
        Matrix xi = Matrix::backSubstitution(matrix, yi);
        for(int j = 0; j < matrix.cols_; j++){
            X[i][j] = xi[j][0];
        }
    }

    return X.transpose();
}

double Matrix::determinant()
{
    double d;
    int s = 0;
    Matrix P = this->LUP();
    for(int i = 0; i < rows_; i++){
        if(P[i][0] != i) s++;
    }
    if(s % 2 == 0){
        d = -1;
    } else {
        d = 1;
    }
    for(int i = 0; i < rows_; i++){
        d *= el[i][i];
    }
    return d;
}

Matrix Matrix::identity(int n)
{
    Matrix t(n, n);
    for(int i = 0; i < n; i++){
        for(int j = 0; j < n; j++){
            if(i == j){
                t.el[i][j] = 1;
            }
        }
    }
    return t;
}

void Matrix::allocate()
{
    el = new double*[rows_];
    for(int i = 0; i < rows_; i++){
        el[i] = new double[cols_];
    }
}


Matrix operator+(const Matrix& matrix1, const Matrix& matrix2)
{
    Matrix sum(matrix1);
    sum += matrix2;
    return sum;
}

Matrix operator-(const Matrix& matrix1, const Matrix& matrix2)
{
    Matrix diff(matrix1);
    diff -= matrix2;
    return diff;
}

Matrix operator*(const Matrix& matrix1, const Matrix& matrix2)
{
    Matrix product(matrix1);
    product *= matrix2;
    return product;
}

Matrix operator*(const Matrix& matrix, double value){
    Matrix product(matrix);
    product *= value;
    return product;
}

Matrix operator*(double value, const Matrix& matrix){
    return matrix * value;
}

