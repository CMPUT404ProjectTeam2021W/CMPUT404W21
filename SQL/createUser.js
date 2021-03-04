// https://www.sqlitetutorial.net/sqlite-nodejs/connect/

const sqlite3 = require('sqlite3').verbose();

// open database in memory
let db = new sqlite3.Database('mysite.db', (err) => {
  if (err) {
    return console.error(err.message);
  }
  console.log('Connected to the in-memory SQlite database.');
});

/**
db.serialize(() => {
    db.each(`SELECT PlaylistId as id,
                    Name as name
             FROM playlists`, (err, row) => {
      if (err) {
        console.error(err.message);
      }
      console.log(row.id + "\t" + row.name);
    });
  });
**/

db.run('INSERT INTO Users VALUES (0, ?, ?)', ['USER1', 'PASSWORD1'], function(err) {
    if (err) {
      return console.log(err.message);
    }
});

// close the database connection
db.close((err) => {
  if (err) {
    return console.error(err.message);
  }
  console.log('Close the database connection.');
});