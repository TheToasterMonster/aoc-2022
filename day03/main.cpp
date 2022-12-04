#include <cctype>
#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_set>

std::vector<std::string> input;

void readFile(const std::string& fp) {
    std::ifstream in(fp);
    while (!in.eof()) {
        std::string line;
        std::getline(in, line);
        input.push_back(line);
    }
}

void part1() {
    long long ans = 0;
    for (const std::string& line : input) {
        std::unordered_set<char> first;
        for (int i = 0; i < line.size() / 2; i++) {
            first.insert(line[i]);
        }
        for (int i = line.size() / 2; i < line.size(); i++) {
            char c = line[i];
            if (first.count(c)) {
                if (std::isupper(c)) {
                    ans += c - 'A' + 27;
                } else {
                    ans += c - 'a' + 1;
                }
                break;
            }
        }
    }
    std::cout << "Part 1: " << ans << "\n";
}

void part2() {
    long long ans = 0;
    for (int i = 0; i < input.size(); i += 3) {
        std::unordered_set<char> first;
        for (char c : input[i]) {
            first.insert(c);
        }
        std::unordered_set<char> firstTwo;
        for (char c : input[i + 1]) {
            if (first.count(c)) {
                firstTwo.insert(c);
            }
        }
        for (char c : input[i + 2]) {
            if (firstTwo.count(c)) {
                if (std::isupper(c)) {
                    ans += c - 'A' + 27;
                } else {
                    ans += c - 'a' + 1;
                }
                break;
            }
        }
    }
    std::cout << "Part 2: " << ans << "\n";
}

const std::string filePath = "./input.txt";

int main() {
    readFile(filePath);
    part1();
    part2();
}
