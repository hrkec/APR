#include <iostream>
#include "Matrix.h"

int main() {

    // 2. zadatak
    std::cout << "2. ZADATAK\n";
    Matrix A("A2.txt");
    Matrix AA = A;
    Matrix b("b2.txt");
    // LU dekompozicija
    A.LU();
    A = AA;
    Matrix P = A.LUP().permutationMatrix();
    Matrix y = Matrix::forwardSubstitution(A, P * b);
    Matrix x = Matrix::backSubstitution(A, y);
    std::cout << "Rjesenje sustava u 2. zadatku : \n" << x << "\n";


    std::cout << "-------------------------------------------------------------------------------------\n";
    std::cout << "3. ZADATAK\n";

    Matrix A3("A3.txt");
    AA = A3;
    Matrix b3("b3.txt");
    A3.LU();
    std::cout << "LU dekompozicija:\n" << A3 << "\n";
    A3 = AA;
    P = A3.LUP().permutationMatrix();
    std::cout << "LUP dekompozicija:\n" << A3 << "\n";
    y = Matrix::forwardSubstitution(A3, P*b3);
    x = Matrix::backSubstitution(A3, y);

    std::cout << "-------------------------------------------------------------------------------------\n";
    std::cout << "4. ZADATAK\n";

    Matrix A4("A4.txt");
    AA = A4;
    Matrix b4("b4.txt");
    A4.LU();
    std::cout << "LU dekompozicija:\n" << A4 << "\n";
    y = Matrix::forwardSubstitution(A4, b4);
    x = Matrix::backSubstitution(A4, y);
    std::cout << "Rjesenje sustava (LU): \n" << x << "\n";

    A4 = AA;
    P = A4.LUP().permutationMatrix();
    std::cout << "LUP dekompozicija:\n" << A4 << "\n";
    y = Matrix::forwardSubstitution(A4, P*b4);
    x = Matrix::backSubstitution(A4, y);
    std::cout << "Rjesenje sustava (LUP): \n" << x << "\n";

    std::cout << "-------------------------------------------------------------------------------------\n";
    std::cout << "5. ZADATAK\n";

    Matrix A5("A5.txt");
    AA = A5;
    Matrix b5("b5.txt");
    A5.LU();
    std::cout << "LU dekompozicija:\n" << A5 << "\n";
    y = Matrix::forwardSubstitution(A5, b5);
    x = Matrix::backSubstitution(A5, y);

    A5 = AA;
    P = A5.LUP().permutationMatrix();
    std::cout << "LUP dekompozicija:\n" << A5 << "\n";
    y = Matrix::forwardSubstitution(A5, P*b5);
    x = Matrix::backSubstitution(A5, y);
    std::cout << "Rjesenje sustava (LUP): \n" << x << "\n";

    std::cout << "-------------------------------------------------------------------------------------\n";
    std::cout << "6. ZADATAK\n";

    Matrix A6("A6.txt");
    AA = A6;
    Matrix b6("b6.txt");

    A6 = AA;
    P = A6.LUP().permutationMatrix();
    std::cout << "LUP dekompozicija:\n" << A6 << "\n";
    y = Matrix::forwardSubstitution(A6, P*b6);
    x = Matrix::backSubstitution(A6, y);
    std::cout << "Rjesenje sustava (LUP): \n" << x << "\n";

    std::cout << "-------------------------------------------------------------------------------------\n";
    std::cout << "7. ZADATAK\n";
    std::cout << "Matrica nema inverz.\n";
    //    Matrix A7("A7.txt");

//    Matrix IN7 = Matrix::inverse(A7);
//    std::cout << "Inverz je  :\n" << IN7;

    std::cout << "-------------------------------------------------------------------------------------\n";
    std::cout << "8. ZADATAK\n";

    Matrix A8("A8.txt");
    Matrix IN8 = Matrix::inverse(A8);
    std::cout << "Inverz je  :\n" << IN8;

    std::cout << "-------------------------------------------------------------------------------------\n";
    std::cout << "9. ZADATAK\n";

    Matrix A9("A9.txt");
    double d9 = A9.determinant();
    std::cout << "Determinanta matrice je " << d9 << ".\n";

    std::cout << "-------------------------------------------------------------------------------------\n";
    std::cout << "10. ZADATAK\n";

    Matrix A10("A10.txt");
    double d10 = A10.determinant();
    std::cout << "Determinanta matrice je " << d10 << ".\n";
}