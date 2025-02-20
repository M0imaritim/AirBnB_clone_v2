# Manifest to setup server for web static

exec {'update':
  provider => shell,
  command  => 'sudo apt-get -y update',
  before   => Exec['install Nginx'],
}

exec {'install Nginx':
  provider => shell,
  command  => 'sudo apt-get -y install nginx',
  before   => Exec['start Nginx'],
}

exec {'start Nginx':
  provider => shell,
  command  => 'sudo service nginx start',
  before   => File['/data/'],
}

# Ensure the /data directory exists and is owned by ubuntu
file {'/data/':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  recurse => true,
  before  => File['/data/web_static/'],
}

# Ensure /data/web_static exists
file {'/data/web_static/':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  before  => [File['/data/web_static/releases/'], File['/data/web_static/shared/']],
}

# Ensure /data/web_static/releases exists
file {'/data/web_static/releases/':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  before  => File['/data/web_static/releases/test/'],
}

# Ensure /data/web_static/shared exists
file {'/data/web_static/shared/':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
}

# Ensure /data/web_static/releases/test exists
file {'/data/web_static/releases/test/':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  before  => File['/data/web_static/releases/test/index.html'],
}

# Create test HTML file
file {'/data/web_static/releases/test/index.html':
  ensure  => file,
  content => 'Holberton School',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
  before  => Exec['symbolic link'],
}

# Create symbolic link
exec {'symbolic link':
  provider => shell,
  command  => 'ln -sf /data/web_static/releases/test/ /data/web_static/current',
  before   => Exec['put location'],
}

# Update Nginx configuration
exec {'put location':
  provider => shell,
  command  => 'sudo sed -i \'48i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}\n\' /etc/nginx/sites-available/default',
  before   => Exec['restart Nginx'],
}

# Restart Nginx to apply changes
exec {'restart Nginx':
  provider => shell,
  command  => 'sudo service nginx restart',
}

