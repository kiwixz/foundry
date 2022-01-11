FROM ubuntu:22.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y upgrade  \
        git ca-certificates  \
        npm make ttfautohint  \
        python3-pip  `# for otf2otc`  \
        curl gcc libc-dev ninja-build  `# for otfcc`

# install otf2otc
RUN pip3 install afdko

# install otfcc
RUN curl -LO "https://github.com/premake/premake-core/releases/download/v5.0.0-alpha15/premake-5.0.0-alpha15-linux.tar.gz"  \
    && tar xf "premake-5.0.0-alpha15-linux.tar.gz" -C "/usr/local/bin"  \
    && rm "premake-5.0.0-alpha15-linux.tar.gz"  \
    && git clone "https://github.com/caryll/otfcc"  \
    && cd "otfcc"  \
    && premake5 ninja  \
    && ninja -C "build/ninja" otfccbuild_release_x64 otfccdump_release_x64  \
    && cp "bin/release-x64/otfccbuild" "bin/release-x64/otfccdump" "/usr/local/bin"  \
    && cd ".."  \
    && rm -rf "otfcc"

ARG IOSEVKA_REF=master
RUN git clone --branch $IOSEVKA_REF --depth 1 "https://github.com/be5invis/iosevka" "/root/iosevka"
WORKDIR "/root/iosevka"

RUN npm install && npm update

COPY "build_plan.toml" "private-build-plans.toml"

RUN npm run build -- "ttf::kiosevka" "woff2::kiosevka"
