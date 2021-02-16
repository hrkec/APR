#ifndef ARP_LAB1_MATRIX_H
#define ARP_LAB1_MATRIX_H

#include <iostream>
#include <string>

class Matrix{
private:
    int rows_, cols_;
    double **el;

    void allocate();

public:
    // Konstruktori
    Matrix();
    Matrix(int, int);
    Matrix(const Matrix&);
    Matrix(const char*);

    //Destruktor
    ~Matrix();

    //Ispis na ekran
    friend std::ostream& operator<<(std::ostream&, const Matrix&);
    //Ispis u datoteku
    void output(const char*);

    //Pristup elementima
    double& operator()(int x, int y);
    double*& operator[](int);

    //Operatori
    Matrix& operator = (const Matrix&);
    Matrix& operator += (const Matrix&);
    Matrix& operator -= (const Matrix&);
    Matrix& operator *= (double);
    Matrix& operator *= (const Matrix&);
    bool operator == (const Matrix&);
    Matrix transpose();

    //Zamjena redaka
    void swapRows(int, int);

    void LU();
    Matrix LUP();
    static Matrix forwardSubstitution(Matrix, Matrix);
    static Matrix backSubstitution(Matrix, Matrix);

    Matrix permutationMatrix();
    double determinant();

    static Matrix inverse(Matrix);
    static Matrix identity(int);
};

Matrix operator+(const Matrix&, const Matrix&);
Matrix operator-(const Matrix&, const Matrix&);
Matrix operator*(const Matrix&, const Matrix&);
Matrix operator*(const Matrix&, double);
Matrix operator*(double, const Matrix&);

#endif //ARP_LAB1_MATRIX_H

