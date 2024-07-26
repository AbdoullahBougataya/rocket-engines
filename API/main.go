package main

import (
    "database/sql"
    "encoding/json"
    "fmt"
    _ "github.com/mattn/go-sqlite3"
    "log"
)
type Vacsl struct {
    Vac   float64    `json:"vaccum"`
    SL    float64    `json:"surface_level"`
}
type Engine struct {
    Id                  int     `json:"id"`
    Engine              string  `json:"engine"`
    Origin              string  `json:"origin"`
    Designer            string  `json:"designer"`
    Vehicle             string  `json:"vehicle"`
    Status              string  `json:"status"`
    Use                 string  `json:"use"`
    Propellant          string  `json:"propellant"`
    Power_cycle         string  `json:"power_cycle"`
    Isp                 Vacsl   `json:"specific_impulse_(s)"`
    Thrust              Vacsl   `json:"thrust_(N)"`
    Chamber_pressure    float64 `json:"chamber_pressure_(bar)"`
    Mass                string  `json:"mass_(kg)"`
    Thrust_weight_ratio float64 `json:"thrust:weight_ratio"`
    Oxidiser_fuel_ratio float64 `json:"oxidiser:fuel_ratio"`
}

func main() {
    db, err := sql.Open("sqlite3", "../db/database.db")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    rows, err := db.Query("SELECT * FROM rocket_engines")
    if err != nil {
        log.Fatal(err)
    }
    defer rows.Close()

    var engines []Engine

    for rows.Next() {
        var engine Engine
        var isp    Vacsl
        var thrust Vacsl
        err := rows.Scan(&engine.Id, &engine.Engine, &engine.Designer, &engine.Origin, &engine.Designer, &engine.Vehicle, &engine.Status, &engine.Use, &engine.Propellant, &engine.Power_cycle, &isp.Vac, &isp.SL, &thrust.Vac, &thrust.SL, &engine.)
        if err != nil {
            log.Fatal(err)
        }
        records = append(records, record)
    }

    if err = rows.Err(); err != nil {
        log.Fatal(err)
    }
