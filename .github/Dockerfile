FROM rust:1.875.0-bookworm
WORKDIR /app
COPY . .
RUN cargo build --release -p simeis-server
EXPOSE 8080
CMD ["./target/release/simeis-server"]