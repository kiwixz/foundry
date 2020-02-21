FROM debian:buster-slim

RUN apt update  \
    && apt -y full-upgrade  \
    && apt -y install  \
        git openssh-client  \
        npm ttfautohint  \
        python3-pip  `# for otf2otc`  \
        curl ninja-build  `# for otfcc`

# install otf2otc
RUN pip3 install afdko

# install otfcc
RUN curl -LO "https://github.com/premake/premake-core/releases/download/v5.0.0-alpha14/premake-5.0.0-alpha14-linux.tar.gz"  \
    && tar xf "premake-5.0.0-alpha14-linux.tar.gz" -C "/usr/local/bin"  \
    && rm "premake-5.0.0-alpha14-linux.tar.gz"  \
    && git clone "https://github.com/caryll/otfcc"  \
    && cd "otfcc"  \
    && premake5 ninja  \
    && ninja -C "build/ninja" otfccbuild_release_x64 otfccdump_release_x64  \
    && cp "bin/release-x64/otfccbuild" "bin/release-x64/otfccdump" "/usr/local/bin"  \
    && cd ".."  \
    && rm -rf "otfcc"

RUN git clone "https://github.com/be5invis/iosevka" "/root/iosevka"
WORKDIR "/root/iosevka"

RUN npm install && npm update

ENTRYPOINT ["npm", "run", "build", "--"]
