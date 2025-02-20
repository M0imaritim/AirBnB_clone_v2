# Update system packages
exec {'update':
  provider => shell,
  command  => 'sudo apt-get -y update',
  before   => Exec['install Nginx'],
}

# Install Nginx
exec {'install Nginx':
  provider => shell,
  command  => 'sudo apt-get -y install nginx',
  before   => Exec['start Nginx'],
}

# Start Nginx service
exec {'start Nginx':
  provider => shell,
  command  => 'sudo service nginx start',
  before   => File['/data/'],
}

# Ensure /data directory exists with correct ownership
file {'/data/':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  recurse => true,
  before  => File['/data/web_static/'],
}

# Ensure /data/web_static exists with correct ownership
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

# Create a test HTML file
file {'/data/web_static/releases/test/index.html':
  ensure  => file,
  content => 'Holberton School',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
  before  => Exec['create symbolic link'],
}

# Create symbolic link and fix ownership
exec {'create symbolic link':
  provider => shell,
  command  => 'ln -sf /data/web_static/releases/test/ /data/web_static/current && sudo chown -h ubuntu:ubuntu /data/web_static/current',
  before   => Exec['put location'],
}

# Ensure Nginx is correctly configured
exec {'put location':
  provider => shell,
  command  => 'sudo sed -i \'/server_name _;/a \\tlocation /hbnb_static/ {\\n\\t\\talias /data/web_static/current/;\\n\\t\\tautoindex off;\\n\\t}\\n\' /etc/nginx/sites-available/default',
  before   => Exec['restart Nginx'],
}

# Restart Nginx to apply configuration changes
exec {'restart Nginx':
  provider => shell,
  command  => 'sudo service nginx restart',
}
