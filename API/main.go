package main

import (
    "database/sql"
    "encoding/json"
    "fmt"
    _ "github.com/mattn/go-sqlite3"
    "log"
    "reflect"
)

// Custom NullValue type
type NullValue struct {
    StringValue string
    FloatValue  float64
    IsString    bool
    Valid       bool
}

// Implement the Scanner interface
func (nv *NullValue) Scan(value interface{}) error {
    if value == nil {
        nv.StringValue, nv.FloatValue, nv.Valid = "", 0.0, false
    } else {
        switch v := value.(type) {
        case string:
            nv.StringValue, nv.IsString, nv.Valid = v, true, true
        case float64:
            nv.FloatValue, nv.IsString, nv.Valid = v, false, true
        default:
            return fmt.Errorf("unsupported type: %v", reflect.TypeOf(value))
        }
    }
    return nil
}

// Implement the Marshaler interface
func (nv NullValue) MarshalJSON() ([]byte, error) {
    if nv.Valid {
        if nv.IsString {
            return json.Marshal(nv.StringValue)
        }
        return json.Marshal(nv.FloatValue)
    }
    return json.Marshal("")
}

type Vacsl struct {
    Vac   float64    `json:"vaccum"`
    SL    float64    `json:"surface_level"`
}
type Engine struct {
    Id                  int     `json:"id"`
    Engine               `json:"engine"`
    Origin               `json:"origin"`
    Designer             `json:"designer"`
    Vehicle              `json:"vehicle"`
    Status               `json:"status"`
    Use                  `json:"use"`
    Propellant           `json:"propellant"`
    Power_cycle          `json:"power_cycle"`
    Isp                 Vacsl   `json:"specific_impulse_(s)"`
    Thrust              Vacsl   `json:"thrust_(N)"`
    Chamber_pressure     `json:"chamber_pressure_(bar)"`
    Mass                 `json:"mass_(kg)"`
    Thrust_weight_ratio  `json:"thrust:weight_ratio"`
    Oxidiser_fuel_ratio  `json:"oxidiser:fuel_ratio"`
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
        err := rows.Scan(&engine.Id, &engine.Engine, &engine.Designer, &engine.Origin, &engine.Designer, &engine.Vehicle, &engine.Status, &engine.Use, &engine.Propellant, &engine.Power_cycle, &isp.Vac, &isp.SL, &thrust.Vac, &thrust.SL, &engine.Chamber_pressure, &engine.Mass, &engine.Thrust_weight_ratio, &engine.Oxidiser_fuel_ratio)
        if err != nil {
            log.Fatal(err)
        }
        engine.Isp = isp
        engine.Thrust = thrust
        engines = append(engines, engine)
    }

    if err = rows.Err(); err != nil {
        log.Fatal(err)
    }
