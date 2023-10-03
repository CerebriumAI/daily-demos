import React, { useState, useEffect } from 'react';
import { useAppMessage } from '@daily-co/daily-react';
import './RiskScore.css';

export default function RiskScore({ id }) {
  const [myScores, setMyScores] = useState();

  useAppMessage({
    onAppMessage: (ev) => {
      console.log(
        'my id: ',
        id,
        ', all risk scores: ',
        ev
      );

      setMyScores(ev.data);

    },
  });

  useEffect(() => {
    if (myScores) {
      console.info(
        myScores
      );
      console.log(myScores.participant)
    }
  }, [myScores]);

  return (
    <div className="riskScores">
      {myScores && id === myScores.participant.replace(/"/g, '') && (
        <div className="riskScore warning">
          <div className="riskLabel">{myScores.message}</div>
        </div>
      )}
    </div>
  );
}
