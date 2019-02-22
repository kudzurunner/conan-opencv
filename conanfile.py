from conans import ConanFile, CMake, tools
import os


class OpencvConan(ConanFile):
    name = "opencv"
    version = "4.0.1"
    license = "https://raw.githubusercontent.com/opencv/opencv/master/LICENSE"
    author = "KudzuRunner"
    url = "https://github.com/kudzurunner/conan-opencv"
    description = "Open Source Computer Vision Library"
    settings = "os", "compiler", "build_type", "arch"

    options = {
        "fPIC": [True, False],
        "with_ocl": [True, False],
        "with_cuda": [True, False],
        "with_eigen": [True, False],
        "with_jasper": [True, False],
        "with_jpeg": [True, False],
        "with_webp": [True, False],
        "with_png": [True, False],
        "with_tbb": [True, False],
        "with_tiff": [True, False],
        "with_lapack": [True, False],
        "with_protobuf": [True, False],
    }

    default_options = {
        "fPIC": True,
        "with_ocl": True,
        "with_cuda": True,
        "with_eigen": True,
        "with_jasper": True,
        "with_jpeg": True,
        "with_webp": True,
        "with_png": True,
        "with_tbb": True,
        "with_tiff": True,
        "with_lapack": True,
        "with_protobuf": True,
    }
    generators = "cmake"

    source_name = "{}-{}".format(name, version)
    install_name = "install"

    exports = (
        "patches/*.patch")

    opencv_libs = [
        "calib3d",
        "core",
        "dnn",
        "features2d",
        "flann",
        "gapi",
        "highgui",
        "imgcodecs",
        "imgproc",
        "ml",
        "objdetect",
        "photo",
        "stitching",
        "video",
        "videoio"]

    all_contrib_libs = [
        "aruco",
        "bgsegm",
        "bioinspired",
        "ccalib",
        "cnn_3dobj",
        "cudaarithm",
        "cudabgsegm",
        "cudacodec",
        "cudafeatures2d",
        "cudafilters",
        "cudaimgproc",
        "cudalegacy",
        "cudaobjdetect",
        "cudaoptflow",
        "cudastereo",
        "cudawarping",
        "cudev",
        "cvv",
        "datasets",
        "dnn_objdetect",
        "dnns_easily_fooled",
        "dpm",
        "face",
        "freetype",
        "fuzzy",
        "hdf",
        "hfs",
        "img_hash",
        "line_descriptor",
        "matlab",
        "optflow",
        "phase_unwrapping",
        "plot",
        "reg",
        "rgbd",
        "saliency",
        "shape",
        "stereo",
        "structured_light",
        "superres",
        "surface_matching",
        "text",
        "tracking",
        "videostab",
        "viz",
        "xfeatures2d",
        "ximgproc",
        "xobjdetect",
        "xphoto"
    ]

    enable_contrib_libs = [
        "cudev"
    ]

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def requirements(self):
        self.requires.add('zlib/1.2.11@conan/stable')
        if self.options.with_eigen:
            self.requires.add('eigen/3.3.7@conan/stable')
        if self.options.with_jasper:
            self.requires.add('jasper/2.0.14@kudzurunner/stable')
        if self.options.with_jpeg:
            self.requires.add('libjpeg-turbo/2.0.1@kudzurunner/stable')
        if self.options.with_webp:
            self.requires.add('libwebp/1.0.0@bincrafters/stable')
        if self.options.with_png:
            self.requires.add('libpng/1.6.36@bincrafters/stable')
        if self.options.with_tbb:
            self.requires.add('TBB/2019_U3@conan/stable')
        if self.options.with_tiff:
            self.requires.add('libtiff/4.0.9@bincrafters/stable')
        if self.options.with_lapack:
            self.requires.add('openblas/0.3.5@kudzurunner/stable')
        if self.options.with_protobuf:
            self.requires.add('protobuf/3.5.1@bincrafters/stable')


    def configure(self):
        if self.settings.os == "Windows":
            self.options["openblas"].visual_studio=True

        self.options["openblas"].shared = True
        self.options["TBB"].tbbmalloc = True
        self.options["jasper"].shared = True
        self.options["libjpeg-turbo"].shared = True
        self.options["libpng"].shared = True
        self.options["libtiff"].shared = True
        self.options["zlib"].shared = True


    def source(self):
        url_template = "https://github.com/opencv/{0}/archive/{1}"
        archive_name = "{}.tar.gz".format(self.version)

        url = url_template.format(self.name, archive_name)
        tools.download(url, filename=archive_name)
        tools.untargz(filename=archive_name)
        os.remove(archive_name)

        name_contrib = self.name + "_contrib"

        url = url_template.format(name_contrib, archive_name)
        tools.download(url, filename=archive_name)
        tools.untargz(filename=archive_name)
        os.remove(archive_name)

        tools.patch(base_path=self.source_name, patch_file="patches/openblas.patch")
        tools.patch(base_path=self.source_name, patch_file="patches/lapack.patch")
        tools.patch(base_path=self.source_name, patch_file="patches/libpng.patch")

        tools.replace_in_file("{}/cmake/OpenCVFindLAPACK.cmake".format(self.source_name),
                              '#message(FATAL_ERROR "LAPACK: check build log:\\n${TRY_OUT}")',
                              'message(FATAL_ERROR "LAPACK: check build log:\\n${TRY_OUT}")')

        tools.replace_in_file("{}/CMakeLists.txt".format(self.source_name),
                              "project(OpenCV CXX C)",
                              """project(OpenCV CXX C)
                                 include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
                                 conan_basic_setup()""")

    def build(self):
        cmake = CMake(self)
        cmake.verbose = True
        cmake.definitions["BUILD_ZLIB"] = "OFF"
        cmake.definitions["BUILD_TIFF"] = "OFF"
        cmake.definitions["BUILD_JASPER"] = "OFF"
        cmake.definitions["BUILD_JPEG"] = "OFF"
        cmake.definitions["BUILD_PNG"] = "OFF"
        cmake.definitions["BUILD_OPENEXR"] = "OFF"
        cmake.definitions["BUILD_WEBP"] = "OFF"
        cmake.definitions["BUILD_TPP"] = "OFF"
        cmake.definitions["BUILD_IPP_IW"] = "OFF"
        cmake.definitions["BUILD_ITT"] = "OFF"
        cmake.definitions["BUILD_PROTOBUF"] = "OFF"

        cmake.definitions["BUILD_SHARED_LIBS"] = "ON"
        cmake.definitions["BUILD_opencv_apps"] = "ON"
        cmake.definitions["BUILD_opencv_js"] = "OFF"
        cmake.definitions["BUILD_ANDROID_PROJECTS"] = "OFF"
        cmake.definitions["BUILD_ANDROID_EXAMPLES"] = "OFF"
        cmake.definitions["BUILD_DOCS"] = "OFF"
        cmake.definitions["BUILD_EXAMPLES"] = "OFF"
        cmake.definitions["BUILD_PACKAGE"] = "OFF"
        cmake.definitions["BUILD_PERF_TESTS"] = "OFF"
        cmake.definitions["BUILD_TESTS"] = "OFF"
        cmake.definitions["BUILD_WITH_DEBUG_INFO"] = "OFF"
        cmake.definitions["BUILD_WITH_STATIC_CRT"] = self.settings.compiler.runtime in ["MT","MTd"]
        cmake.definitions["BUILD_WITH_DYNAMIC_IPP"] = "OFF"
        cmake.definitions["BUILD_FAT_JAVA_LIB"] = "OFF"
        cmake.definitions["BUILD_ANDROID_SERVICE"] = "OFF"
        cmake.definitions["BUILD_CUDA_STUBS"] = "OFF"
        cmake.definitions["BUILD_JAVA"] = "OFF"
        cmake.definitions["BUILD_QUIRC"] = "OFF"

        cmake.definitions["WITH_OPENCL"] = self.options.with_ocl
        cmake.definitions["WITH_CUDA"] = self.options.with_cuda
        cmake.definitions["WITH_VTK"] = "OFF"
        cmake.definitions["WITH_EIGEN"] = self.options.with_eigen
        cmake.definitions["WITH_FFMPEG"] = "OFF"
        cmake.definitions["WITH_GSTREAMER"] = "OFF"
        cmake.definitions["WITH_GTK"] = "OFF"
        cmake.definitions["WITH_IPP"] = "OFF"
        cmake.definitions["WITH_JASPER"] = self.options.with_jasper
        cmake.definitions["WITH_JPEG"] = self.options.with_jpeg
        cmake.definitions["WITH_WEBP"] = self.options.with_webp
        cmake.definitions["WITH_OPENEXR"] = "OFF"
        cmake.definitions["WITH_PNG"] = self.options.with_png
        cmake.definitions["WITH_QT"] = "OFF"
        cmake.definitions["WITH_TBB"] = self.options.with_tbb
        cmake.definitions["WITH_TIFF"] = self.options.with_tiff
        cmake.definitions["WITH_V4L"] = "OFF"
        cmake.definitions["WITH_DSHOW"] = "OFF"
        cmake.definitions["WITH_MSMF"] = "OFF"
        cmake.definitions["WITH_LAPACK"] = self.options.with_lapack
        cmake.definitions["WITH_ITT"] = "OFF"
        cmake.definitions["WITH_PROTOBUF"] = self.options.with_protobuf
        cmake.definitions["WITH_QUIRC"] = "OFF"

        #
        cmake.definitions["BUILD_opencv_python2"] = "OFF"
        cmake.definitions["BUILD_opencv_python3"] = "OFF"
        cmake.definitions["BUILD_opencv_java"] = "OFF"
        cmake.definitions["BUILD_opencv_ts"] = "OFF"
        cmake.definitions["BUILD_opencv_world"] = "OFF"

        for lib in self.all_contrib_libs:
            cmake.definitions["BUILD_opencv_{}".format(lib)] = "OFF"

        for lib in self.enable_contrib_libs:
            cmake.definitions["BUILD_opencv_{}".format(lib)] = "ON"

        cmake.definitions["OPENCV_EXTRA_MODULES_PATH"] = os.path.join(self.source_folder, "opencv_contrib-{}".format(self.version), "modules")
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = "install"

        cmake.configure(source_folder=self.source_name)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="*.h*", dst="include", src =os.path.join(self.install_name, "include"), keep_path=True)
        self.copy(pattern="*.lib", dst="lib", src=self.install_name, keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
        self.copy(pattern="*.exe", dst="bin", src="bin", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src=self.install_name, keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=self.install_name, keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src=self.install_name, keep_path=False)

    def package_info(self):
        libs = []
        for name in self.opencv_libs + self.enable_contrib_libs:
            libs.append("opencv_{}".format(name))

        opencv_version_suffix = self.version.replace(".","")
        if self.settings.compiler == "Visual Studio":
            debug_suffix = ("d" if self.settings.build_type=="Debug" else "")
            self.cpp_info.libs.extend([n + opencv_version_suffix + debug_suffix for n in libs])

        self.cpp_info.includedirs.append(os.path.join('include', 'opencv4'))
        self.cpp_info.libdirs.append(os.path.join('lib', 'opencv4', '3rdparty'))
