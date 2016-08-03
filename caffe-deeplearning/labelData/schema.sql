drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  image_id integer not null,
  'tag' text not null,
  'created_at' DATETIME DEFAULT CURRENT_TIMESTAMP
);
