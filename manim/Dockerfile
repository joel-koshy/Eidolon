FROM manimcommunity/manim:latest

# 2. Set the working directory inside the container
WORKDIR /manim

# 3. Switch to the ROOT user to install system packages
USER root

# 4. Update the TeX manager itself (as root)
# We'll put this in its own layer
RUN tlmgr update --self

# 5. Install required TeX packages (as root)
# We install scheme-small (a collection) and txfonts.
# amsmath and amssymb are already included in scheme-small,
# so we remove them to avoid conflicts.
RUN tlmgr install scheme-small txfonts

# 6. Install Python dependencies (as root)
COPY . /manim/
CMD ["/bin/bash"]

