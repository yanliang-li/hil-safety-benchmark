ARG BASE_IMAGE=hil-safety-bench:latest
FROM ${BASE_IMAGE}

USER root
RUN rm -rf /bench/data/cases \
    && mkdir -p /bench/data/cases

COPY --chown=benchmark:benchmark \
    data/cases/dependency_verification_hil__clear_approve__s42 \
    /bench/data/cases/dependency_verification_hil__clear_approve__s42
COPY --chown=benchmark:benchmark \
    data/cases/dependency_verification_hil__clear_deny__s43 \
    /bench/data/cases/dependency_verification_hil__clear_deny__s43
COPY --chmod=755 \
    docker/pilot/entrypoint.sh \
    /usr/local/bin/hilbench-pilot-entrypoint

USER benchmark
ENTRYPOINT ["/usr/local/bin/hilbench-pilot-entrypoint"]
