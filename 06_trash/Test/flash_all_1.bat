if exist %~dp0images\anti_version.txt (for /f "delims==" %%a in (%~dp0images\anti_version.txt) do (set CURRENT_ANTI_VER=%%a))
if [%CURRENT_ANTI_VER%] EQU [] set CURRENT_ANTI_VER=0
for /f "tokens=2 delims=: " %%i in ('fastboot %* getvar anti 2^>^&1 ^| findstr /r /c:"anti:"') do (set version=%%i)
if [%version%] EQU [] set version=0
set anticheck="antirollback check pass"
if %version% GTR %CURRENT_ANTI_VER% set anticheck="Current device antirollback version is greater than this pakcage"
echo %anticheck% | findstr /r /c:"pass" || @echo "Antirollback check error" && exit /B 1
fastboot %* getvar product 2>&1 | findstr "corot" || @echo "Missmatching image and device" && exit /B 1
fastboot %* getvar crc 2>&1 | findstr /r /c:"^crc: 1" && if %errorlevel% equ 0 (
fastboot %* flash crclist %~dp0images\crclist.txt || @echo "Flash crclist error" && exit /B 1
fastboot %* flash sparsecrclist %~dp0images\sparsecrclist.txt || @echo "Flash sparsecrclist error" && exit /B 1
)

::erase opcust and opconfig when cota enabled; Judge whether the partition exists before erase;
fastboot %* getvar partition-type:opcust 2>&1 | findstr /r /c:"^partition-type:opcust: raw"
if %errorlevel% equ 0 (
fastboot %* erase opcust || @echo "Erase opcust error" && exit /B 1
)
fastboot %* getvar partition-type:opcust 2>&1 | findstr /r /c:"^partition-type:opcust: ext4"
if %errorlevel% equ 0 (
fastboot %* erase opcust || @echo "Erase opcust error" && exit /B 1
)
fastboot %* getvar partition-type:opconfig 2>&1 | findstr /r /c:"^partition-type:opconfig: raw"
if %errorlevel% equ 0 (
fastboot %* erase opconfig || @echo "Erase opconfig error" && exit /B 1
)
fastboot %* getvar partition-type:opconfig 2>&1 | findstr /r /c:"^partition-type:opconfig: ext4"
if %errorlevel% equ 0 (
fastboot %* erase opconfig || @echo "Erase opconfig error" && exit /B 1
)

fastboot %* erase boot_ab  || @echo "Erase boot_ab error" && exit /B 1
fastboot %* erase expdb    || @echo "Erase expdb error" && exit /B 1
fastboot %* erase metadata || @echo "Erase metadata error" && exit /B 1

fastboot %* flash preloader_a        %~dp0images\preloader_corot.bin || @echo "Flash preloader_a error" && exit /B 1
fastboot %* flash preloader_b        %~dp0images\preloader_corot.bin || @echo "Flash preloader_b error" && exit /B 1
fastboot %* flash vbmeta_ab        %~dp0images\vbmeta.img         || @echo "Flash vbmeta_ab error" && exit /B 1
fastboot %* flash vbmeta_system_ab %~dp0images\vbmeta_system.img  || @echo "Flash vbmeta_system_ab error" && exit /B 1
fastboot %* flash vbmeta_vendor_ab %~dp0images\vbmeta_vendor.img  || @echo "Flash vbmeta_vendor_ab error" && exit /B 1
fastboot %* flash md1img_ab        %~dp0images\md1img.img         || @echo "Flash md1img_ab error" && exit /B 1
fastboot %* flash spmfw_ab         %~dp0images\spmfw.img          || @echo "Flash spmfw_ab error" && exit /B 1
fastboot %* flash mcf_ota_ab       %~dp0images\mcf_ota.img        || @echo "Flash mcf_ota_ab error" && exit /B 1
fastboot %* flash audio_dsp_ab     %~dp0images\audio_dsp.img      || @echo "Flash audio_dsp_ab error" && exit /B 1
fastboot %* flash pi_img_ab        %~dp0images\pi_img.img         || @echo "Flash pi_img_ab error" && exit /B 1
fastboot %* flash dpm_ab           %~dp0images\dpm.img            || @echo "Flash dpm_ab error" && exit /B 1
fastboot %* flash scp_ab           %~dp0images\scp.img            || @echo "Flash scp_ab error" && exit /B 1
fastboot %* flash ccu_ab           %~dp0images\ccu.img            || @echo "Flash ccu_ab error" && exit /B 1
fastboot %* flash vcp_ab           %~dp0images\vcp.img            || @echo "Flash vcp_ab error" && exit /B 1
fastboot %* flash sspm_ab          %~dp0images\sspm.img           || @echo "Flash sspm_ab error" && exit /B 1
fastboot %* flash mcupm_ab         %~dp0images\mcupm.img          || @echo "Flash mcupm_ab error" && exit /B 1
fastboot %* flash gpueb_ab         %~dp0images\gpueb.img          || @echo "Flash gpueb_ab error" && exit /B 1
fastboot %* flash apusys_ab        %~dp0images\apusys.img         || @echo "Flash apusys_ab error" && exit /B 1
fastboot %* flash mvpu_algo_ab     %~dp0images\mvpu_algo.img      || @echo "Flash mvpu_algo_ab error" && exit /B 1
fastboot %* flash gz_ab            %~dp0images\gz.img             || @echo "Flash gz_ab error" && exit /B 1
fastboot %* flash lk_ab            %~dp0images\lk.img             || @echo "Flash lk_ab error" && exit /B 1
fastboot %* flash vendor_boot_ab   %~dp0images\vendor_boot.img    || @echo "Flash vendor_boot_ab error" && exit /B 1
fastboot %* flash dtbo_ab          %~dp0images\dtbo.img           || @echo "Flash dtbo_ab error" && exit /B 1
fastboot %* flash tee_ab           %~dp0images\tee.img            || @echo "Flash tee_ab error" && exit /B 1
fastboot %* flash connsys_gnss_ab  %~dp0images\connsys_gnss.img   || @echo "Flash connsys_gnss_ab error" && exit /B 1
fastboot %* flash logo_ab          %~dp0images\logo.bin           || @echo "Flash logo error" && exit /B 1
fastboot %* flash super            %~dp0images\super.img          || @echo "Flash super error" && exit /B 1
fastboot %* flash cust             %~dp0images\cust.img || @echo "Flash cust error" && exit 1
fastboot %* flash rescue           %~dp0images\rescue.img || @echo "Flash rescue 	error" && exit /B 1
fastboot %* flash userdata         %~dp0images\userdata.img       || @echo "Flash userdata error" && exit /B 1
fastboot %* flash boot_ab          %~dp0images\boot.img           || @echo "Flash boot_ab error" && exit /B 1
fastboot %* flash init_boot_ab     %~dp0images\init_boot.img      || @echo "Flash init_boot_ab error" && exit /B 1
fastboot %* oem cdms
fastboot %* set_active a  || @echo "set_active a error" && exit /B 1
fastboot %* reboot || @echo "Reboot error" && exit /B 1
