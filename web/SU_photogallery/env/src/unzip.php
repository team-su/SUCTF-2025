<?php
/*
 * @Author: Nbc
 * @Date: 2025-01-13 16:13:46
 * @LastEditors: Nbc
 * @LastEditTime: 2025-01-13 16:31:53
 * @FilePath: \src\unzip.php
 * @Description: 
 * 
 * Copyright (c) 2025 by Nbc, All Rights Reserved. 
 */
error_reporting(0);

function get_extension($filename){
    return pathinfo($filename, PATHINFO_EXTENSION);
}
function check_extension($filename,$path){
    $filePath = $path . DIRECTORY_SEPARATOR . $filename;
    
    if (is_file($filePath)) {
        $extension = strtolower(get_extension($filename));

        if (!in_array($extension, ['jpg', 'jpeg', 'png', 'gif'])) {
            if (!unlink($filePath)) {
                // echo "Fail to delete file: $filename\n";
                return false;
                }
            else{
                // echo "This file format is not supported:$extension\n";
                return false;
                }
    
        }
        else{
            return true;
            }
}
else{
    // echo "nofile";
    return false;
}
}
function file_rename ($path,$file){
    $randomName = md5(uniqid().rand(0, 99999)) . '.' . get_extension($file);
                $oldPath = $path . DIRECTORY_SEPARATOR . $file;
                $newPath = $path . DIRECTORY_SEPARATOR . $randomName;

                if (!rename($oldPath, $newPath)) {
                    unlink($path . DIRECTORY_SEPARATOR . $file);
                    // echo "Fail to rename file: $file\n";
                    return false;
                }
                else{
                    return true;
                }
}

function move_file($path,$basePath){
    foreach (glob($path . DIRECTORY_SEPARATOR . '*') as $file) {
        $destination = $basePath . DIRECTORY_SEPARATOR . basename($file);
        if (!rename($file, $destination)){
            // echo "Fail to rename file: $file\n";
            return false;
        }
      
    }
    return true;
}


function check_base($fileContent){
    $keywords = ['eval', 'base64', 'shell_exec', 'system', 'passthru', 'assert', 'flag', 'exec', 'phar', 'xml', 'DOCTYPE', 'iconv', 'zip', 'file', 'chr', 'hex2bin', 'dir', 'function', 'pcntl_exec', 'array', 'include', 'require', 'call_user_func', 'getallheaders', 'get_defined_vars','info'];
    $base64_keywords = [];
    foreach ($keywords as $keyword) {
        $base64_keywords[] = base64_encode($keyword);
    }
    foreach ($base64_keywords as $base64_keyword) {
        if (strpos($fileContent, $base64_keyword)!== false) {
            return true;

        }
        else{
           return false;

        }
    }
}

function check_content($zip){
    for ($i = 0; $i < $zip->numFiles; $i++) {
        $fileInfo = $zip->statIndex($i);
        $fileName = $fileInfo['name'];
        if (preg_match('/\.\.(\/|\.|%2e%2e%2f)/i', $fileName)) {
            return false; 
        }
            // echo "Checking file: $fileName\n";
            $fileContent = $zip->getFromName($fileName);
            

            if (preg_match('/(eval|base64|shell_exec|system|passthru|assert|flag|exec|phar|xml|DOCTYPE|iconv|zip|file|chr|hex2bin|dir|function|pcntl_exec|array|include|require|call_user_func|getallheaders|get_defined_vars|info)/i', $fileContent) || check_base($fileContent)) {
                // echo "Don't hack me!\n";    
                return false;
            }
            else {
                continue;
            }
        }
    return true;
}

function unzip($zipname, $basePath) {
    $zip = new ZipArchive;

    if (!file_exists($zipname)) {
        // echo "Zip file does not exist";
        return "zip_not_found";
    }
    if (!$zip->open($zipname)) {
        // echo "Fail to open zip file";
        return "zip_open_failed";
    }
    if (!check_content($zip)) {
        return "malicious_content_detected";
    }
    $randomDir = 'tmp_'.md5(uniqid().rand(0, 99999));
    $path = $basePath . DIRECTORY_SEPARATOR . $randomDir;
    if (!mkdir($path, 0777, true)) {
        // echo "Fail to create directory";
        $zip->close();
        return "mkdir_failed";
    }
    if (!$zip->extractTo($path)) {
        // echo "Fail to extract zip file";
        $zip->close();
    }
    else{
        for ($i = 0; $i < $zip->numFiles; $i++) {
            $fileInfo = $zip->statIndex($i);
            $fileName = $fileInfo['name'];
            if (!check_extension($fileName, $path)) {
                // echo "Unsupported file extension";
                continue;
            }
            if (!file_rename($path, $fileName)) {
                // echo "File rename failed";
                continue;
            }
        }
    }

    if (!move_file($path, $basePath)) {
        $zip->close();
        // echo "Fail to move file";
        return "move_failed";
    }
    rmdir($path);
    $zip->close();
    return true;
}


$uploadDir = __DIR__ . DIRECTORY_SEPARATOR . 'upload/suimages/';
if (!is_dir($uploadDir)) {
    mkdir($uploadDir, 0777, true);
}

if (isset($_FILES['file']) && $_FILES['file']['error'] === UPLOAD_ERR_OK) {
    $uploadedFile = $_FILES['file'];
    $zipname = $uploadedFile['tmp_name'];
    $path = $uploadDir;

    $result = unzip($zipname, $path);
    if ($result === true) {
        header("Location: index.html?status=success");
        exit();
    } else {
        header("Location: index.html?status=$result");
        exit();
    }
} else {
    header("Location: index.html?status=file_error");
    exit();
}