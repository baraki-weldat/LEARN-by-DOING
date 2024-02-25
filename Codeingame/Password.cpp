#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

/**
 * 
 * 
 **/

int main()
{
    int a;
    int b;
    int c;
    cin >> a >> b >> c; cin.ignore();

    // Write an answer using cout. DON'T FORGET THE "<< endl"
    // To debug: cerr << "Debug messages..." << endl;
    // METHOD-1: Unoptimized Solution
    int count=0;
    for(int i = 0; i<=a;i++){
        for(int j = 0; j<=b; j++){
            for(int k = 0; k <= c; k++){
                count+=1;

            }
        }
    }
    cout << count << endl;
    // METHOD-2: Optimized Solution based on the Mathematical Formula
    cout<< (a+1)*(b+1)*(c+1) << endl; 

}