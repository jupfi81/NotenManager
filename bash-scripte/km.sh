#!/bin/bash
while [ -n "$1" ]; do
  case "$1" in
    --open) 
      param="$2"
      echo "open file <$param>"
      cd ~/$param
      shift
      ;;
    *) echo "Option $1 not recognized";;
  esac
  shift
done
