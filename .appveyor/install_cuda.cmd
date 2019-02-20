@echo on

appveyor DownloadFile ^
  https://developer.nvidia.com/compute/cuda/8.0/Prod2/local_installers/cuda_8.0.61_win10-exe ^
  -FileName cuda_setup.exe
appveyor DownloadFile ^
   https://developer.nvidia.com/compute/cuda/8.0/Prod2/patches/2/cuda_8.0.61.2_windows-exe ^
   -FileName cuda_patch.exe
appveyor Downloadfile ^
  http://developer.download.nvidia.com/compute/redist/cudnn/v7.0.4/cudnn-8.0-windows10-x64-v7.zip ^
  -FileName cudnn.zip

7z x cuda_setup.exe -ocuda_8.0
cd cuda_8.0
setup.exe -s compiler_8.0 cublas_8.0 cublas_dev_8.0 cudart_8.0 cufft_8.0 cufft_dev_8.0 curand_8.0 curand_dev_8.0 cusolver_8.0 cusolver_dev_8.0 cusparse_8.0 cusparse_dev_8.0 nvrtc_8.0 nvrtc_dev_8.0

cd ..

7z x cuda_patch.exe -ocuda_patch_8.0
cd cuda_patch_8.0
setup.exe -s cublas_8.0 cublas_dev_8.0

cd ..

set PATH=%ProgramFiles%\NVIDIA GPU Computing Toolkit\CUDA\v8.0\bin;%ProgramFiles%\NVIDIA GPU Computing Toolkit\CUDA\v8.0\libnvvp;%PATH%

nvcc -V

if NOT EXIST "%ProgramFiles%\NVIDIA GPU Computing Toolkit\CUDA\v8.0\bin\cudart64_80.dll" (
echo "Failed to install CUDA"
exit /B 1
)

7z x cudnn.zip
copy cuda\include\cudnn.h ^
  "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v8.0\include\"
copy cuda\lib\x64\cudnn.lib ^
  "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v8.0\lib\x64\"
copy cuda\bin\cudnn64_7.dll ^
  "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v8.0\bin\"

nvcc -V

cd %APPVEYOR_BUILD_FOLDER%