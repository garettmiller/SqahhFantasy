import './App.css';
import React from 'react';

function App() {
  return (<div className="App">
    <Header/>
    <MatchSection/>
    <ScoringRulesSection/>
    <SectionHeader title="Season Standings"/>
    </div>
  );
}

class Header extends React.Component {
  render() {
    return (
      <div>
        <header className="App-header Header">
          Sqahh Fantasy
        </header>
        <div className="App-subheader Header">
          The Official Newsletter of Sqahh's Kicker Union
        </div>
      </div>
      
    );
  }
}

class MatchSection extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      items: []
    };
  }

  componentDidMount() {
    fetch("http://127.0.0.1:5000/")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            matches: result.matches,
            week: result.week
          });
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }

  render() {

    const { error, isLoaded, matches, week } = this.state;
    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    };

    const matchcomps = matches.map((match)=>{
      return <Match match={match}/>;
    });

    const title = "Week " + week + " Matchup";

  return (<div>
    <SectionHeader title={title}/>
    {matchcomps}
    </div>);
  }
}

class SectionHeader extends React.Component {
  render() {
    return (
        <div className="SectionHeader Header">
            {this.props.title}
        </div>
    );
  }
}

class Match extends React.Component {
  render() {

    const match = this.props.match
    const homeTeamName = match.home_team.team_name;
    const homeTeamKickerName = match.home_team.player_name;

    const homeScore = match.home_team.total_score
    const awayScore = match.away_team.total_score

    const awayTeamName = match.away_team.team_name;
    const awayTeamKickerName = match.away_team.player_name;

    const homeTeamBreakdown = match.home_team.score_breakdown;
    const awayTeamBreakdown = match.away_team.score_breakdown;

    return (
      <div className="Match">
        <TeamPerformance teamName={homeTeamName} total_score={homeScore} breakdown={homeTeamBreakdown} kickerName={homeTeamKickerName}/>
        <TeamPerformance teamName="vs"/>
        <TeamPerformance teamName={awayTeamName} total_score={awayScore} breakdown={awayTeamBreakdown} kickerName={awayTeamKickerName}/>
      </div>
    );
  }
}

class TeamPerformance extends React.Component {
    render() {
      var breakdownDisplay = "";
      if (this.props.breakdown){
        breakdownDisplay = this.props.breakdown.map((item)=>{
          return <li className="BreakDown">{item}</li>;
        });
      }

      const title = this.props.teamName + (this.props.kickerName ? " (" + this.props.kickerName + "): "  + this.props.total_score : "");

      return (
        <div className="TeamPerformance">
          <div className="MatchHeader Header">
            {title}
          </div>
          <div>
            {breakdownDisplay}
          </div>
        </div>
      );
    }
}

class ScoringRulesSection extends React.Component {
  render() {
      return (<div>
        <SectionHeader title="Scoring Rules"/>
        <ScoringRules style={{justify:"center"}}/>
      </div>
      );
  }
}

class ScoringRules extends React.Component {
  render() {
    return (
      <div className="RulesList">
      <li className="BreakDown">Successful PAT: 1 pt</li>
      <li className="BreakDown">Successful Kick &lt;40 yds: 3 pts</li>
      <li className="BreakDown">Successful Kick 40-49 yds: 4 pts</li>
      <li className="BreakDown">Successful Kick 50-59 yds: 6 pts</li>
      <li className="BreakDown">Successful Kick &gt;60 yds: 8 pts</li>
      <li className="BreakDown">Failed Kick: -2 pts</li>
      <li className="BreakDown">Tackle: 5 pts</li>
      <li className="BreakDown">Successful Game Winning Kick: Value is doubled</li>
      </div>
    );
  }
}



export default App;
