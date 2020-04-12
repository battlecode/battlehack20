import React, { Component } from 'react';
import $ from 'jquery';
import Api from '../api';
import { NavLink, Link } from 'react-router-dom';
import Countdown from './countdown';
import UpdateCard from '../components/updateCard';
import PerfCard from '../components/perfCard';

class StatCard extends UpdateCard {
    componentDidMount() {
        $().ready(function() {
            Api.getTeamWinStats(function(stats) {
                window.Chartist.Pie('#stat_chart', {
                    labels: stats,
                    series: stats
                }); 
            });
        });
    }

    render() {
        return (
            <div className="card">
                <div className="header">
                    <h4 className="title">Match Statistics</h4>
                    <p className="category">Wins and losses.</p>
                </div>
                <div className="content">
                    <div id="stat_chart" className="ct-chart ct-perfect-fourth" />
                    <div className="footer">
                        <div className="legend">
                            <i className="fa fa-circle text-info" /> Win
                            <span style={{marginLeft: "10px"}}> </span>
                            <i className="fa fa-circle text-danger" /> Loss
                        </div>
                        <hr />
                        { this.getFooter() }
                    </div>
                </div>
            </div>
        );
    }
}

class DateCard extends UpdateCard {
    constructor() {
        super();
        this.state.dates = [];
    }

    componentDidMount() {
        Api.getUpdates(function(dates) {
            this.setState({ dates: (dates.length > 5)?dates.slice(0,5):dates  });
            if (dates[0]) {
                console.log(dates[0].dateObj)
                this.setState({update_date: dates[0].dateObj})
            }
        }.bind(this));
    }

    render() {
        return (
            <div className="card ">
                <div className="header">
                    <h4 className="title">Recent Updates</h4>
                    <p className="category">A full listing can be found in the sidebar.</p>
                </div>
                <div className="content">
                    <div className="table-full-width">
                        <table className="table">
                            <tbody>
                                { this.state.dates.map(date => <tr key={ date.id }>
                                <td>{ date.time }</td>
                                <td>{ date.message }</td>
                                </tr> )}
                            </tbody>
                        </table>
                    </div>
                    { this.getFooter() }
                </div>
            </div>
        );
    }
}

class InstrCard extends UpdateCard {
    constructor() {
        super();
        this.state.dates = [];
    }

    componentDidMount() {
        // meh
    }

    render() {
        return (
            <div className="card ">
                <div className="header">
                    <h4 className="title">Welcome to Battlehack 2020!</h4>
                </div>
                <div className="content">
                    <p>
                        🍜. Be sure to look at the getting started section for information on how to get the game and your first bot running! 
                    </p>
                </div>
            </div>
        );
    }
}


class LinksCard extends Component {
    constructor() {
        super();
    }

    componentDidMount() {
        // meh
    }
      

    render() {
        return (
            <div className="card ">
                <div className="header">
                    <h4 className="title">Useful Links</h4>
                </div>
                <div className="content">
                    <p>
                        <ul>
                            <li>
                                <a href="https://discordapp.com/channels/386965718572466197/650084292982079539">Discord</a> (<a href="https://discord.gg/N86mxkH">invite</a>)
                            </li>
                            <li>
                                <a href='https://github.com/battlecode/battlecode20'>GitHub</a>
                            </li>
                            <li>
                                <a href='https://twitch.tv/mitbattlecode'>Twitch</a>
                            </li>
                            <li>
                                <a href='https://battlecode.org'>Battlecode.org</a>
                            </li>
                        </ul>
                    </p>
                </div>
            </div>
        );
    }
}

class Home extends Component {
    constructor() {
        super();
        this.state = {on_team:null};
    }

    componentDidMount() {
        Api.getUserTeam(function(e) {
            this.setState({on_team:(e !== null)});
        }.bind(this));
    }

    render() {
        return (
            <div className="content">
                <div className="container-fluid">
                    <div className="row">
                        <div className="col-md-6">
                            <div className="container-fluid">
                                <div className="row">
                                        <InstrCard />
                                </div>
                                <div className="row">
                                        <Countdown />
                                </div>
                                <div className="row">
                                        {this.state.on_team && <StatCard />}
                                </div>
                            </div>
                        </div>
                        <div className="col-md-6">
                            <div className="container-fluid">
                                <div className="row">
                                        <DateCard />
                                </div>
                                <div className="row">
                                        <LinksCard />
                                </div>
                                <div className="row">
                                        {this.state.on_team && <PerfCard team={null} />}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default Home;
