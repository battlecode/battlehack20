import React, { Component } from 'react';
import Api from '../api';
import { NavLink } from 'react-router-dom';

class Tournament extends Component {
    render() {
        return (<div>
<p dangerouslySetInnerHTML={{__html: this.props.blurb}}>
            </p>
                        <h5 className="mb-0">
                            <button className="btn btn-default btn-block collapsed" type="button" data-toggle="collapse" data-target={ '#' + this.props.name.replace(' ','') + '0'}>
                                { this.props.name.charAt(0).toUpperCase() + this.props.name.slice(1) } Tournament Bracket
                            </button>
                        </h5>
                    <div id={ this.props.name.replace(' ','') + '0' } className="collapse" data-parent={ '#' + this.props.name } style={{ 'margin-top':'-1em' }}>
                        <div className="card-body">
                            <iframe title={ this.props.challonge } src={this.props.challonge + "/module"} width="100%" height="400px" frameborder="0" scrolling="auto" allowtransparency="true"></iframe>
                        </div>
                    </div>
                    </div>
        );
    }
}

class Tournaments extends Component {
    constructor() {
        super();
        this.state = {'tournaments':[]};
    }

    componentDidMount() {
        Api.getTournaments(function(t) {
            this.setState({tournaments:t});
        }.bind(this));
    }

    render() {
        return (
            <div className="content">
                <div className="container-fluid">
                    <div className="row">
                        <div className="col-md-12">

                            <div className="card">
                                <div className="header">
                                    <h4 className="title">Tournament Results</h4>
                                </div>
                                <div className="content">
                                    <p>
                                        Thank you to everyone for participating!
                                    </p>
                                    <p>
                                        <b>The winner of Battlehack 2020 is <NavLink to='rankings/1643'>Team Snakes and ladders</NavLink></b>, 
                                        awarded a cash prize of $500. Congrats!
                                        </p>
                                    <p>
                                        The full results of the round robin of the top 16 teams, with replays, <a href='https://bh2020.battlecode.org/finalresults.json'>are available here</a>.
                                    </p>
                                    <p>The results of the 4 divisions for determining the top 16 are available here: <a href='https://docs.google.com/spreadsheets/d/1n0aUFyXv_IEvvYum5QvjxIsbYUZPwADfcdee04dej84/edit?usp=sharing'>here</a></p>
                                    <p>
                                        <b>Engine breaker winners:</b>
                                        <ul>
                                            <li>
                                            <a href='https://github.com/battlecode/battlehack20/issues/133'>Issue 133</a>: $125
                                            </li>
                                            <li>
                                            <a href='https://github.com/battlecode/battlehack20/issues/121'>Issue 121</a>: $125
                                            </li>
                                            <li>
                                            <a href='https://github.com/battlecode/battlehack20/issues/108'>Issue 108</a>: $100
                                            </li>
                                            <li>
                                            <a href='https://github.com/battlecode/battlehack20/issues/106'>Issue 106</a>: $100
                                            </li>
                                            <li>
                                            <a href='https://github.com/battlecode/battlehack20/issues/104'>Issue 104</a>: $100
                                            </li>
                                            <li>
                                            <a href='https://github.com/battlecode/battlehack20/issues/97'>Issue 97</a>: $100
                                            </li>
                                            <li>
                                            <a href='https://github.com/battlecode/battlehack20/issues/71'>Issue 71</a>: $100
                                            </li>
                                        </ul>
                                    </p>
                                    <p>
                                        <b>L33t h4ck3r winners:</b>
                                        <ul>
                                            <li>
                                            <a href='https://github.com/battlecode/battlehack20/issues/136'>Issue 136</a>: $350
                                            </li>
                                            <li>
                                            <a href='https://github.com/battlecode/battlehack20/issues/69'>Issue 69</a>: $200
                                            </li>
                                            <li>
                                            <a href='https://github.com/battlecode/battlehack20/issues/135'>Issue 135</a>: $200
                                            </li>
                                        </ul>
                                    </p>
                                </div>
                            </div>

                            <div className="card">
                                <div className="header">
                                    <h4 className="title">Tournament Schedule</h4>
                                </div>
                                <div className="content">

                                    <p>
                                        Battlehack 2020 will start on <b>Thursday, April 16th at 8pm MIT time (EDT +5mins)</b> and consist of one tournament at the end of the week-long event.
                                    </p>

                                    <p>
                                        The deadline to submit code for this final tournament is <b>Wednesday, April 22nd at 8pm EDT</b>.
                                    </p>

                                    <p>
                                        We will stream and commentate this tournament on <b>Friday, April 24th at 8pm EDT</b>.
                                    </p>
                                </div>
                            </div>


                            <div className="card">
                                <div className="header">
                                    <h4 className="title">Tournament Format</h4>
                                </div>
                                <div className="content">
                                    <p>
                                        In response to competitor feedback, we have changed the format of the competition.
                                        Teams are split into four divisions. Round Robin tournaments are held within each of these divisions.
                                        From each division, the four teams with the highest win-ratio move on the the next round.
                                        These top 16 will face eachother in another round-robin tournament.
                                    </p>
                                </div>
                            </div>

                            <div className='card'>
                                <div className='header'>
                                    <h4 className='title'>Results</h4>
                                </div>
                                <div className='content'>
                                    <p>Division Results are out!</p>
                                </div>

                            </div>


                            <div className="card">
                                <div className="header">
                                    <h4 className="title">Prizes</h4>
                                </div>
                                <div className="content">
                                    <p>
                                        Thanks to our sponsor HRT!
                                        
                                        <ul>
                                            <li><b>$500 1st Place prize:</b> to whosoever has the highest rating at the end (hacks not allowed)</li>
                                            
                                            <li><b>$750 Engine Breaker prize:</b> for finding major bugs (e.g. getting illegal game state, crashing opponents, giving yourself unlimited bytecode, etc). A list of bugs known before launch can be found <a href="https://docs.google.com/document/d/10Id1pa7txfkrFgaM7WrK90VQKdbCXlNDOUuMRx7x9ls/edit?usp=sharing">here</a>; duplicating these bugs will not result in any prizes awarded. This prize will be split across all teams who submit a novel reproducible example as a GitHub issue <a href="https://github.com/battlecode/battlehack20/issues">here</a>.</li>
                                            
                                            <li><b>$750 L33t H4ck3r prize:</b> escape the sandbox into our servers. 
                                            Split across all teams who contact us and demonstrate a unique exploit, that can either read the value
                                            of an environment variable (e.g. <code>echo $SECRET_KEY</code>) or read the contents of an arbitrary
                                            file (e.g. <code>open("api_key.json","r")</code>).
                                            Please do NOT submit them publicly (i.e. no GitHub issue). Email us or DM us on Discord.
                                            </li>
                                            
                                            <li><b>More prizes???</b> TBA, maybe</li>
                                        </ul>
                                    </p>
                                </div>
                            </div>



                            <div className="card">
                                <div className="header">
                                    <h4 className="title">Eligibility Rules</h4>
                                </div>
                                <div className="content">
                                    <p>
                                        Anyone is welcome to participate in Battlecode! Anyone can write a bot, create a team and participate in the tournament. 
                                    </p>
                                    
                                    <p>
                                        Only current full-time students (both college and high school) are eligible for prizes.
                                    </p>
                                    
                                    <p>
                                        Contact us on <a href='https://discordapp.com/channels/386965718572466197/650097270804709436'>Discord</a> or at <a href='mailto:battlecode@mit.edu'>battlecode@mit.edu</a> if you are unsure of your eligibility.
                                    </p>

                                </div>
                            </div>


                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default Tournaments;
