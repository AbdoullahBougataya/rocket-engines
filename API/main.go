package main

import (
    "database/sql"
    "encoding/json"
    "fmt"
    _ "github.com/mattn/go-sqlite3"
    "log"
)
type Vacsl struct {
    Vac   int    `json:"vaccum"`
    SL    int    `json:"surface_level"`
}
type Record struct {
    Id          int    `json:"id"`
    Engine      string `json:"engine"`
    Origin      string `json:"origin"`
    Designer    string `json:"designer"`
    Vehicle     string `json:"vehicle"`
    Status      string `json:"status"`
    Use         string `json:"use"`
    Propellant  string `json:"propellant"`
    Power_cycle string `json:"power_cycle"`
    Isp_vac    int    `json:"specific impulse vaccum (s)"`
    Isp_sl    int    `json:"specific impulse surface level (s)"`
    Thrust_vac    int    `json:"id"`
    Thrust_sl    int    `json:"id"`
}

func main() {
    db, err := sql.Open("sqlite3", "./your-database.db")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    rows, err := db.Query("SELECT id, name, email FROM your_table")
    if err != nil {
        log.Fatal(err)
    }
    defer rows.Close()

    var records []Record

    for rows.Next() {
        var record Record
        err := rows.Scan(&record.ID, &record.Name, &record.Email)
        if err != nil {
            log.Fatal(err)
        }
        records = append(records, record)
    }

    if err = rows.Err(); err != nil {
        log.Fatal(err)
    }
