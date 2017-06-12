#!/usr/bin/env bash

export PACKAGE_NAME="shortly"
export VERSION=$(<VERSION)
export ALIAS="v$( (echo ${VERSION}) | sed s/\\./_/g)"
export ARTIFACTS="`pwd`/artifact"

echo "Building ${VERSION} of ${PACKAGE_NAME}"
echo "----------------------------------------------------"
echo "cleaning up previous"
rm -rf build $ARTIFACTS

echo "creating build directory"
mkdir -p build $ARTIFACTS

echo "copying code"
cp -r ${PACKAGE_NAME} build/

echo "installing requirements"
pip install -t ./build -r requirements.txt

echo "zip it up"
cd build
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
zip -r ${ARTIFACTS}/${PACKAGE_NAME}-v${VERSION}.zip *
cd ..

echo "${PACKAGE_NAME}/v${VERSION}.zip"
echo "publishing to S3"
aws s3 cp ${ARTIFACTS}/${PACKAGE_NAME}-v${VERSION}.zip "s3://ds.io-builds/${PACKAGE_NAME}/v${VERSION}.zip"

echo "DONE"
