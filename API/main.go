package main

import (
	"database/sql"
	"fmt"
	"github.com/mattn/go-sqlite3"
	"net/http"
	"github.com/gin-gonic/gin"
	"errors"
)

func main()
{
	database, err = sql.Open("sqlite3", "../db/database.db");
	if err != nil {
        fmt.Println("Error opening database:", err)
        return
    }
    defer db.Close()

	rows, err := database.Query("SELECT * FROM rocket_engines")
    if err != nil {
        fmt.Println("Error performing query:", err)
        return
    }
    defer rows.Close()
}
