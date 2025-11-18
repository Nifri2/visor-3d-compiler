{
  description = "Protogen :3";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs?ref=nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";


  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        overlays = [  ];
        pkgs = import nixpkgs { inherit system overlays; };

        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          pyyaml
          pillow
          numpy
          rich
        ]);

        # Cross-compilation for RPi Zero 2 W (aarch64)
        target = "aarch64-unknown-linux-gnu";

      in {
        devShells.default = pkgs.mkShell {
          nativeBuildInputs = [
            pkgs.python3
            pkgs.micropython
            pkgs.rshell
            pkgs.mpy-utils
            pkgs.adafruit-ampy
            pkgs.picocom
            pkgs.picotool
          ];

          shellHook = ''
            fish --init-command 'source .dev-fish-setup.fish'
            exit 0
          '';

          buildInputs = [
            pythonEnv
            pkgs.libclang
          ];
        };
      }
    );
}