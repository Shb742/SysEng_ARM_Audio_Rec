# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Gradually shifting towards complete offline deployment.

## [1.5.0] - 2019-04-09
### Changed
- Added install.sh script. It detects whether Node.js and MongoDB has already been installed. Written in bash script and tested.
- Moving out the modifying .env part to a CLI located in ./bin, when module is installed globally, this CLI can automatically be added to PATH.

## [1.4.0] - 2019-04-07
### Added
- Changelog will be maintained from now on.
- A ready-to-deploy, platform-independent version of EDVS Dashboard will be shown on [release page](https://github.com/Shb742/SysEng_ARM_Audio_Rec/releases).

### Changed
- Switched from [bcrypt](https://www.npmjs.com/package/bcrypt) to [bcryptjs](https://www.npmjs.com/package/bcryptjs) to better support offline cross-platform compatibility and offline installation. However, performance has seen a ~30% decrease.

## [1.3.0] - 2019-04-06
### Added
- [memorystore](https://www.npmjs.com/package/memorystore) added to prevent potential memory leak due to excessive cookie information store.

## [1.2.0] - 2019-03-29
### Changed
- Moved Helmet.js middleware to before the routing-HTTP-to-HTTPS middleware to prevent the initial 301 response header revealing any weakness.
- Removed the lastModified header when serving static webpages and files.
- Temporarily disabled HSTS.

### Removed
- The [body-parser](https://www.npmjs.com/package/body-parser) module as Express.js already incorporated the module. Reduce project dependency.
- Removed the initial implementation of the dictionary.

## [1.0.0] - 2017-06-20
### Added
- Initial release of EDVS Dashboard.

[Unreleased]: https://github.com/Shb742/SysEng_ARM_Audio_Rec
