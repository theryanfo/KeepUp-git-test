import { useState } from 'react'
import './App.css'
import LoginButton from './LoginButton';
import LogoutButton from './LogoutButton';

// import React from 'react';
// import NewPlaylist from './NewPlaylist';
// import BlockedArtists from './BlockedArtists';
// import BlockedTracks from './BlockedTracks';
import GeneratePlaylistButton from './GeneratePlaylistButton';
import TestButton from './TestButton';
// import TestButton from './TestButton';
// import SearchArtists from './SearchArtists';
// import SearchTracks from './SearchTracks';

const App = () => {
  return (
    <div className="main-container">
      <LoginButton />
      <LogoutButton />
      <TestButton />

      {/* 
      <TestButton />

      <NewPlaylist />
      <BlockedArtists />
      <BlockedTracks />
      <GeneratePlaylistButton />
      <SearchArtists />
      <SearchTracks />      
      */}


    </div>
  );
};

export default App;
