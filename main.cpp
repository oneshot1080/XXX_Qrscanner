#include <iostream>
#include <algorithm>
#include <vector>

int main(int argc, char const *argv[])
{
    std::cout << "Hello World\n";
    std::vector<int> arr = {1, 2, 3, 4, 9, 7};
    std::sort(arr.begin(), arr.end());
    for (auto &&i : arr)
    {
        std::cout << i << " ";
    }
    
    return 0;
}


int cal(int &a);