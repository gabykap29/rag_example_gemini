#!/bin/bash
set -e

ollama serve &

sleep 10

ollama pull nomic-embed-text:latest || true

wait
