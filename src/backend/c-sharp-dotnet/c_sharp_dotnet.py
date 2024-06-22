import os
import click
import subprocess

def run_command(command):
    """Runs a shell command and prints the output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    result.check_returncode()

def create_solution(solution_name):
    """Creates a new .NET solution."""
    run_command(f'dotnet new sln -n {solution_name}')

def create_api_project(project_name, solution_name):
    """Creates a new .NET API project and adds it to the solution."""
    run_command(f'dotnet new webapi -n {project_name}')
    run_command(f'dotnet sln {solution_name}.sln add {project_name}/{project_name}.csproj')

def add_entity_framework(project_name):
    """Adds Entity Framework Core to the project."""
    run_command(f'dotnet add {project_name}/{project_name}.csproj package Microsoft.EntityFrameworkCore')
    run_command(f'dotnet add {project_name}/{project_name}.csproj package Microsoft.EntityFrameworkCore.SqlServer')
    run_command(f'dotnet add {project_name}/{project_name}.csproj package Microsoft.EntityFrameworkCore.Tools')

def create_initial_model(project_name):
    """Creates an initial Entity Framework model."""
    models_dir = os.path.join(project_name, "Models")
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    
    model_content = '''using System;
using Microsoft.EntityFrameworkCore;

namespace Models
{
    public class ApplicationDbContext : DbContext
    {
        public DbSet<SampleEntity> SampleEntities { get; set; }

        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }
    }

    public class SampleEntity
    {
        public int Id { get; set; }
        public string Name { get; set; }
    }
}'''
    
    with open(os.path.join(models_dir, "ApplicationDbContext.cs"), 'w') as f:
        f.write(model_content)

def update_startup_file(project_name):
    """Updates the Startup.cs file to use Entity Framework."""
    startup_file = os.path.join(project_name, "Startup.cs")
    with open(startup_file, 'r') as f:
        content = f.read()
    
    new_content = content.replace(
        "public void ConfigureServices(IServiceCollection services)",
        '''public void ConfigureServices(IServiceCollection services)
        {
            services.AddDbContext<Models.ApplicationDbContext>(options =>
                options.UseSqlServer(Configuration.GetConnectionString("DefaultConnection")));
        '''
    )

    with open(startup_file, 'w') as f:
        f.write(new_content)

def create_appsettings_file(project_name):
    """Creates the appsettings.json file with a default connection string."""
    appsettings_content = '''{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\\\mssqllocaldb;Database=EFCoreSample;Trusted_Connection=True;MultipleActiveResultSets=true"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*"
}'''
    
    appsettings_file = os.path.join(project_name, "appsettings.json")
    with open(appsettings_file, 'w') as f:
        f.write(appsettings_content)

@click.command()
@click.argument('solution_name')
@click.argument('project_name')
def cli(solution_name, project_name):
    """CLI to initialize a .NET server with Entity Framework."""
    create_solution(solution_name)
    create_api_project(project_name, solution_name)
    add_entity_framework(project_name)
    create_initial_model(project_name)
    update_startup_file(project_name)
    create_appsettings_file(project_name)
    print(f'Successfully created .NET solution {solution_name} with API project {project_name} and Entity Framework setup.')

if __name__ == '__main__':
    cli()

