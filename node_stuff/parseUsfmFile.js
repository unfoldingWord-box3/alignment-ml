/**
 * This script updates the resources in a given directory for the given languages
 * Syntax: node scripts/resources/updateResources.js <path to resources> <language> [language...]
 */
const path = require('path-extra');
const fs = require('fs-extra');
const PackageParseHelpers = require('tc-source-content-updater').packageParseHelpers;

/**
 * iterate through process arguments and separate out flags and other parameters
 * @return {{flags: [], otherParameters: []}}
 */
function separateParams() {
  const flags = [];
  const otherParameters = [];

  for (let i = 2, l = process.argv.length; i < l; i++) {
    const param = process.argv[i];

    if (param.substr(0, 1) === '-') { // see if flag
      flags.push(param);
    } else {
      otherParameters.push(param);
    }
  }
  return { flags, otherParameters };
}

/**
 * see if flag is in flags
 * @param {Array} flags
 * @param {String} flag - flag to match
 * @return {Boolean}
 */
function findFlag(flags, flag) {
  const found = flags.find((item) => (item === flag));
  return !!found;
}

// run as main
if (require.main === module) {
  const { flags, otherParameters } = separateParams();

  if (otherParameters.length < 2) {
    console.error('Syntax: node ./parseUsfmFile.js sourceUsfmPath outputJsonPath');
    process.exitCode = 1;
    return 1;
  }

  const sourceUsfmPath = otherParameters[0];
  const outputJsonPath = otherParameters[1];

  console.log(`Parsing {sourceUsfmPath} to ${outputJsonPath}`);

  try {
    PackageParseHelpers.parseUsfmOfBook(sourceUsfmPath, outputJsonPath);
    process.exitCode = 0;
  } catch(e) {
    console.error(`Failed to parse {sourceUsfmPath} to ${outputJsonPath}`);
    process.exitCode = 1;
  }
}
