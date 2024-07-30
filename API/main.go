package main

import (
    "database/sql"
    "encoding/json"
    "fmt"
    _ "github.com/mattn/go-sqlite3"
    "log"
    "reflect"
    "net/http"
    "strconv"
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
    Engine              string  `json:"engine"`
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

func welcome_handler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintln(w, "Welcome to rocket engines API 🚀.")
}

func handler(w http.ResponseWriter, r *http.Request) {
    // Parse query parameters
    q_engine := r.URL.Query().Get("engine")
    id_str := r.URL.Query().Get("id")

    // Convert id from string to int
    var id int
    var err error
    if id_str != "" {
        id, err = strconv.Atoi(id_str)
        if err != nil {
            http.Error(w, "Invalid id parameter", http.StatusBadRequest)
            return
        }
    }

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

    // Filter data based on query parameters
    var filtered_data []Engine
    if q_engine != "" && id_str != "" {
        for _, item := range engines {
            if q_engine != "" && item.Engine != q_engine && item.Id != id {
                continue
            }
            filtered_data = append(filtered_data, item)
        }
    } else if q_engine != "" {
        for _, item := range engines {
            if q_engine != "" && item.Engine != q_engine {
                continue
            }
            filtered_data = append(filtered_data, item)
        }
    } else if id_str != "" {
	    for _, item := range engines {
	        if id_str != "" && item.Id != id {
                continue
            }
	        filtered_data = append(filtered_data, item)
	    }
    } else {
        filtered_data = engines
    }
    // Respond with the parsed data
    json_data, err := json.Marshal(filtered_data)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    w.Header().Set("Content-Type", "application/json")
    w.Write(json_data)
}

func main() {
    http.HandleFunc("/welcome", welcome_handler)
    http.HandleFunc("/engines", handler)
    fmt.Println("Server is running on port 8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
