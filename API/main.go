package main

import (
    "database/sql"
    "encoding/json"
    "fmt"
    _ "github.com/mattn/go-sqlite3"
    "log"
    "reflect"
    "net/http"
)

// I used the help of AI in this section

// Custom NullValue type
type NullValue struct {
    StringValue string
    FloatValue  float64
    IsString    bool
    Valid       bool
}

// DB instance
var db *sql.DB

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
// End

type Vacsl struct {
    Vac   NullValue    `json:"vaccum"`
    SL    NullValue    `json:"surface_level"`
}
type Engine struct {
    Id                  int     `json:"id"`
    Engine              NullValue `json:"engine"`
    Origin              NullValue `json:"origin"`
    Designer            NullValue `json:"designer"`
    Vehicle             NullValue `json:"vehicle"`
    Status              NullValue `json:"status"`
    Use                 NullValue `json:"use"`
    Propellant          NullValue `json:"propellant"`
    Power_cycle         NullValue `json:"power_cycle"`
    Isp                 Vacsl   `json:"specific_impulse_(s)"`
    Thrust              Vacsl   `json:"thrust_(N)"`
    Chamber_pressure    NullValue `json:"chamber_pressure_(bar)"`
    Mass                NullValue `json:"mass_(kg)"`
    Thrust_weight_ratio NullValue `json:"thrust:weight_ratio"`
    Oxidiser_fuel_ratio NullValue `json:"oxidiser:fuel_ratio"`
}

func handler(w http.ResponseWriter, r *http.Request) {
    db, err := sql.Open("sqlite3", "../db/database.db")

    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    defer db.Close()

    rows, err := db.Query("SELECT * FROM rocket_engines")
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    defer rows.Close()

    var engines []Engine
    for rows.Next() {
        var engine Engine
        var isp    Vacsl
        var thrust Vacsl

        err := rows.Scan(&engine.Id, &engine.Engine, &engine.Origin, &engine.Designer, &engine.Vehicle, &engine.Status, &engine.Use, &engine.Propellant, &engine.Power_cycle, &isp.Vac, &isp.SL, &thrust.Vac, &thrust.SL, &engine.Chamber_pressure, &engine.Mass, &engine.Thrust_weight_ratio, &engine.Oxidiser_fuel_ratio)
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        engine.Isp = isp
        engine.Thrust = thrust
        engines = append(engines, engine)
    }

    err = rows.Err()
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    // Respond with the parsed data
    json_data, err := json.Marshal(engines)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    json_string = string(json_data)
    w.Header().Set("Content-Type", "application/json")
    w.Write(json_data)
}

func main() {
    http.HandleFunc("/engines", handler)
    fmt.Println("Server is running on port 8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
