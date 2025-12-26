FROM rust:1.82 as builder

WORKDIR /app

COPY Cargo.toml Cargo.lock* ./

COPY src ./src

RUN cargo build --release

FROM debian:bookworm-slim

STOPSIGNAL SIGTERM

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/target/release/sim-device .

COPY .env* ./

CMD ["./sim-device"]
