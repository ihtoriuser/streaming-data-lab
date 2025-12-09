$libDir = ".\lib"
if (!(Test-Path -Path $libDir)) {
    New-Item -ItemType Directory -Path $libDir
}

$jars = @(
    @{
        Url = "https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/1.17.1/flink-sql-connector-kafka-1.17.1.jar"
        Name = "flink-sql-connector-kafka-1.17.1.jar"
    },
    @{
        Url = "https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/3.1.0-1.17/flink-connector-jdbc-3.1.0-1.17.jar"
        Name = "flink-connector-jdbc-3.1.0-1.17.jar"
    },
    @{
        Url = "https://jdbc.postgresql.org/download/postgresql-42.6.0.jar"
        Name = "postgresql-42.6.0.jar"
    }
)

foreach ($jar in $jars) {
    $outputPath = Join-Path -Path $libDir -ChildPath $jar.Name
    if (!(Test-Path -Path $outputPath)) {
        Write-Host "Downloading $($jar.Name)..."
        Invoke-WebRequest -Uri $jar.Url -OutFile $outputPath
    } else {
        Write-Host "$($jar.Name) already exists."
    }
}

Write-Host "All JARs downloaded to $libDir"
