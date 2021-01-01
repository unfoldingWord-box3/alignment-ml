import sys
import os
import platform
import subprocess


def printSystemInfo():
    print("#### System Info ####")
    print(f"  sys.version:  {sys.version}")
    print(f"  sys.version_info:  {sys.version_info}")
    print(f"  platform.python_version():  {platform.python_version()}")
    print(f"  platform.architecture():  {platform.architecture()}")
    print(f"  platform.machine():  {platform.machine()}")
    print(f"  platform.platform():  {platform.platform()}")
    print(f"  platform.processor():  {platform.processor()}")
    print(f"  platform.python_compiler():  {platform.python_compiler()}")
    print(f"  platform.python_implementation():  {platform.python_implementation()}")
    print(f"  platform.system():  {platform.system()}\n")

def createNodeDownloadCommand(cfg, base_url_of_resource, destination_folder, languageId, resourceId, version, resource_name):
    # [flags] base_url_of_resource destination_folder languageId, resourceId, version
    baseLangResourceUrl = cfg['baseLangResourceUrl']
    cmd = ['node','./downloadResource.js']
    if base_url_of_resource != baseLangResourceUrl:
        cmd.append('--fullUrl')
    cmd.extend([base_url_of_resource, destination_folder, languageId, resourceId, version, resource_name])
    return cmd

def downloadAndProcessResource(cfg, base_url_of_resource, destination_folder, languageId, resourceId, version, resource_name):
    cmd = createNodeDownloadCommand(cfg, base_url_of_resource, destination_folder, languageId, resourceId, version, resource_name)
    runNodeCommand(cmd)

def createNodeUsfmConvertCommand(sourceUsfmPath, outputJsonPath):
    cmd = ['node','./parseUsfmFile.js']
    sourceUsfmPath = sourceUsfmPath.replace('./', '../')
    outputJsonPath = outputJsonPath.replace('./', '../')
    cmd.extend([sourceUsfmPath, outputJsonPath])
    return cmd

def convertUsfmToJson(sourceUsfmPath, outputJsonPath):
    cmd = createNodeUsfmConvertCommand(sourceUsfmPath, outputJsonPath)
    runNodeCommand(cmd)

def runNodeCommand(cmd):
    cwd = os.getcwd()
    os.chdir("./node_stuff")
    print(f"Downloading and processing {cmd}")
    process = subprocess.run(cmd,
                             stderr=subprocess.PIPE,
                             universal_newlines=True)
    os.chdir(cwd)
    returncode = process.returncode
    if returncode > 0:
        print("\n\n################\nError\n################")
        print(process.stderr)
        exit(returncode)

    print(f"Finished processing {cmd}")

