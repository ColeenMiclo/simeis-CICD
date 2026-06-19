release:
	RUSTFLAGS="-C code-model=kernel -C codegen-units=1"
	cargo build --release -p simeis-server
	strip target/release/simeis-server

doc:
	# Create documentation for the project
	typst compile README.md

check:
	# Check code
	cargo check --workspace --all-targets

test:
	# Run unit tests
	cargo test --workspace

clean:
	# Clean up build files
	cargo clean
