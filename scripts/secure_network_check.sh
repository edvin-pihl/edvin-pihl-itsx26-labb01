#!/bin/bash

# Secure Network Check
# Syfte: kontrollera grundläggande nätverksfunktioner i den egna Linuxmiljön.
# Säkerhetsavgränsning: skriptet arbetar endast mot localhost,
# lokala portar och ett definierat domännamn.
# Ingen extern portskanning genomförs.

DOMAIN="example.com"
TEST_PORT="8080"
LOG_DIR="$HOME/secure-network-logs"

SUCCESS=0
FAILED=0

mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/network_check_$(date '+%Y-%m-%d_%H-%M-%S').log"

log_message() {
    local status="$1"
    local message="$2"

    echo "[$status] $message"
    echo "$(date '+%Y-%m-%d_%H-%M-%S') [$status] $message" >> "$LOG_FILE"
}

check_environment() {
    log_message "INFO" "Kontrollerar nätverksmiljö"

    echo "--- IP-adresser ---" >> "$LOG_FILE"
    ip address >> "$LOG_FILE" 2>&1

    echo "--- Routing ---" >> "$LOG_FILE"
    ip route >> "$LOG_FILE" 2>&1

    if ip route | grep -q "^default"; then
        log_message "OK" "Default route hittades"
        ((SUCCESS++))
    else
        log_message "WARN" "Ingen default route hittades"
        ((FAILED++))
    fi
}

check_dns() {
    log_message "INFO" "Kontrollerar DNS för $DOMAIN"

    if [ -z "$DOMAIN" ]; then
        log_message "FAIL" "Domännamnet är tomt"
        ((FAILED++))
        return 1
    fi

    if getent hosts "$DOMAIN" >> "$LOG_FILE" 2>&1; then
        log_message "OK" "DNS-uppslag fungerade för $DOMAIN"
        ((SUCCESS++))
        return 0
    else
        log_message "FAIL" "DNS-uppslag misslyckades för $DOMAIN"
        ((FAILED++))
        return 1
    fi
}

check_ports() {
    log_message "INFO" "Kontrollerar lokalt lyssnande portar"

    if command -v ss >/dev/null 2>&1; then
        ss -tuln >> "$LOG_FILE" 2>&1
        log_message "OK" "Portöversikt skapades"
        ((SUCCESS++))
    else
        log_message "FAIL" "Kommandot ss saknas"
        ((FAILED++))
    fi
}

check_local_service() {
    log_message "INFO" "Kontrollerar localhost på port $TEST_PORT"

    if curl --silent --fail --max-time 3 \
        "http://127.0.0.1:$TEST_PORT" >/dev/null; then

        log_message "OK" "Lokal tjänst svarar på port $TEST_PORT"
        ((SUCCESS++))
        return 0
    else
        log_message "FAIL" "Ingen lokal tjänst svarar på port $TEST_PORT"
        ((FAILED++))
        return 1
    fi
}

cleanup() {
    log_message "INFO" "Cleanup genomfört"
}

summary() {
    echo
    echo "=============================="
    echo " Secure Network Check"
    echo "=============================="
    echo "Lyckades: $SUCCESS"
    echo "Misslyckades: $FAILED"
    echo "Loggfil: $LOG_FILE"
}

SAFE_CHECKS=(
    "check_environment"
    "check_dns"
    "check_ports"
    "check_local_service"
)

log_message "INFO" "Secure Network Check startar"

for check in "${SAFE_CHECKS[@]}"; do
    "$check"
done

cleanup
summary

if [ "$FAILED" -gt 0 ]; then
    exit 1
else
    exit 0
fi

cleanup
summary

if [ "$FAILED" -gt 0 ]; then
    exit 1
else
    exit 0
fi