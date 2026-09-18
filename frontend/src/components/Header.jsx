export default function Header() {
  return (
    <header className="topbar">

      <div className="brandArea">

        <div className="brand">
          AirResolve
        </div>

        <div className="brandSubtitle">
          Policy-Grounded Airline Resolution Agent
        </div>

      </div>


      <div className="headerRight">

        <div className="systemBadge">
          <span className="statusDot"></span>
          Grounded Mode
        </div>

      </div>

    </header>
  );
}