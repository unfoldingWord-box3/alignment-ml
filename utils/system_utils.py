import sys
import os
import platform
import subprocess


def printSystemInfo():
    print("#### System Info ####")
    print(f"  python platform.python_version():  {platform.python_version()}")
    print(f"  python sys.version:  {sys.version}")
    print(f"  python platform.platform():  {platform.platform()}\n")

def createNodeDownloadCommand(cfg, base_url_of_resource, destination_folder, languageId, resourceId, version, resource_name):
    # [flags] base_url_of_resource destination_folder languageId, resourceId, version
    baseLangResourceUrl = cfg['baseLangResourceUrl']
    cmd = ['node','./downloadResource.js', '--ignoreMissingProjects']
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

def runCommand(cmd, ignoreOutput=False):
    print(f"Running {cmd}")
    if ignoreOutput:
        process = subprocess.run(cmd,
                                 stderr=subprocess.PIPE,
                                 text=True,
                                 universal_newlines=True)
    else:
        process = subprocess.run(cmd,
                                 capture_output=True, text=True,
                                 universal_newlines=True)
    returncode = process.returncode
    if returncode > 0:
        print("\n\n################\nError\n################")
        print(process.stderr)
        exit(returncode)

    print(f"Finished {cmd}")
    return process.stdout

def pipInstall(package):
    print(f"Installing package {package}")
    error = None
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    except Exception as e:
        error = e

    if error:
        error = None
        try:
            print("pip install failed, trying conda")
            runCommand(["conda", "install", "-y", package], ignoreOutput=True)
        except Exception as e:
            error = e

    if error:
        print("\n\n################\nError\n################")
        print(error)
        exit()

    print(f"Installed {package}")

