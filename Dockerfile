FROM your_base_image

# Other instructions...

RUN python --version

ENV NIXPACKS_PATH /opt/venv/bin:$NIXPACKS_PATH
COPY . /app/.

RUN --mount=type=cache,id=s/4af3bd69-c477-456e-aee9-af4aa3d351ab-/root/cache/pip,target=/root/.cache/pip python -m venv --copies /opt/venv && . /opt/venv/bin/activate && pip install -r requirements.txt
