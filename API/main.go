package main

import (
	"database/sql"
	"github.com/mattn/go-sqlite3"
	"net/http"
	"github.com/gin-gonic/gin"
	"errors"
)

func main()
{
	database, _ = sql.Open("sqlite3", "../db/database.db");
}
