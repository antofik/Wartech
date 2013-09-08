var colors = [
    '', 'orange', 'brown', 'red', 'green', 'blue', 'yellow', 'white'
];
function Team()
{
    Team.teams_count = Team.teams_count || 0;
    Team.teams_count++;
    this.color = colors[Team.teams_count];
}