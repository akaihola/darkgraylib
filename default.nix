{ pkgs ? import <nixpkgs> { } }:
(
  pkgs.stdenv.mkDerivation {
    name = "darkgraylib-test";
    buildInputs = [ pkgs.python311 pkgs.git pkgs.uv ];
  }
)
