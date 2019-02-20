#include <iostream>
#include <opencv2/opencv.hpp>

int main() {
    cv::Mat mat = cv::Mat::zeros(10, 10, CV_64F);
    std::cout << mat.size() << std::endl;
    return 0;
}
