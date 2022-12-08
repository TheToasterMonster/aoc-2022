#include <algorithm>
#include <fstream>
#include <iostream>
#include <vector>

const std::string INPUT_FILE = "./input.txt";
std::vector<std::string> grid;
std::vector<std::vector<int>> visible;

void readInput() {
    std::ifstream in(INPUT_FILE);
    while (!in.eof()) {
        std::string s;
        in >> s;
        if (s.size() > 0) {
            grid.push_back(s);
        }
    }
    visible = std::vector<std::vector<int>>(grid.size(), std::vector<int>(grid[0].size(), 0));
}

void part1() {
    // left to right
    for (int i = 0; i < grid.size(); i++) {
        char currMax = 0;
        for (int j = 0; j < grid[0].size(); j++) {
            if (grid[i][j] > currMax) {
                visible[i][j] = 1;
                currMax = grid[i][j];
            }
        }
    }

    // right to left
    for (int i = 0; i < grid.size(); i++) {
        char currMax = 0;
        for (int j = grid[0].size() - 1; j >= 0; j--) {
            if (grid[i][j] > currMax) {
                visible[i][j] = 1;
                currMax = grid[i][j];
            }
        }
    }

    // top to bottom
    for (int j = 0; j < grid[0].size(); j++) {
        char currMax = 0;
        for (int i = 0; i < grid.size(); i++) {
            if (grid[i][j] > currMax) {
                visible[i][j] = 1;
                currMax = grid[i][j];
            }
        }
    }

    // bottom to top
    for (int j = 0; j < grid[0].size(); j++) {
        char currMax = 0;
        for (int i = grid.size() - 1; i >= 0; i--) {
            if (grid[i][j] > currMax) {
                visible[i][j] = 1;
                currMax = grid[i][j];
            }
        }
    }

    long long count = 0;
    for (auto& row : visible) {
        for (int i : row) {
            count += i;
        }
    }
    std::cout << "Part 1: " << count << "\n";
}

long long score(int i, int j) {
    if (i == 0 || i == grid.size() - 1 || j == 0 || j == grid[0].size() - 1) {
        return 0;
    }

    int down = 1;
    while (i + down < grid.size() - 1 && grid[i+down][j] < grid[i][j]) {
        down++;
    }

    int up = 1;
    while (i - up > 0 && grid[i-up][j] < grid[i][j]) {
        up++;
    }

    int right = 1;
    while (j + right < grid[0].size() - 1 && grid[i][j+right] < grid[i][j]) {
        right++;
    }

    int left = 1;
    while (j - left > 0 && grid[i][j-left] < grid[i][j]) {
        left++;
    }

    return (long long) down * up * right * left;
}

void part2() {
    long long best = 0;
    for (int i = 0; i < grid.size(); i++) {
        for (int j = 0; j < grid[0].size(); j++) {
            best = std::max(best, score(i, j));
        }
    }
    std::cout << "Part 2: " << best << "\n";
}

int main() {
    readInput();
    part1();
    part2();
}
