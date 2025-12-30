#include <iostream>
#include <string>
#include <vector>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <netdb.h>
#include <cstring>
#include <chrono>
#include <thread>
#include <mutex>

// SHΔDØW CORE C++ MODULE
// TARGET: FAST TCP CONNECT SCAN

std::mutex print_mutex;

bool port_is_open(const std::string& address, int port) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) return false;

    sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    inet_pton(AF_INET, address.c_str(), &server_addr.sin_addr);

    // Set timeout
    struct timeval tv;
    tv.tv_sec = 1;
    tv.tv_usec = 0;
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, (const char*)&tv, sizeof tv);
    setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, (const char*)&tv, sizeof tv);

    int result = connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr));
    close(sock);
    return result == 0;
}

void scan_range(const std::string& target, int start_port, int end_port, std::vector<int>& open_ports) {
    for (int port = start_port; port <= end_port; ++port) {
        if (port_is_open(target, port)) {
            std::lock_guard<std::mutex> lock(print_mutex);
            std::cout << "\033[1;34m[+] FOUND KERNEL ENTRY: PORT " << port << " OPEN\033[0m" << std::endl;
            open_ports.push_back(port);
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " <IP> <START_PORT> <END_PORT>" << std::endl;
        return 1;
    }

    std::string target_ip = argv[1];
    int start_port = std::stoi(argv[2]);
    int end_port = std::stoi(argv[3]);

    std::cout << "\033[1;30m[SHΔDØW_CPP] INITIATING HYPER-THREADED SCAN ON " << target_ip << "...\033[0m" << std::endl;

    std::vector<int> open_ports;
    // Simple single threaded for now to ensure stability, can be upgraded to multi-threaded
    scan_range(target_ip, start_port, end_port, open_ports);

    return 0;
}
