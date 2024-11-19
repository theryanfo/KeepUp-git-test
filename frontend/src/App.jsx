import { useState } from 'react'

import './App.css'

// import React from 'react';
// import NewPlaylist from './NewPlaylist';
// import BlockedArtists from './BlockedArtists';
// import BlockedTracks from './BlockedTracks';
import GeneratePlaylistButton from './GeneratePlaylistButton';
import TestButton from './TestButton';
// import SearchArtists from './SearchArtists';
// import SearchTracks from './SearchTracks';

const MainContainer = () => {
  return (
    <div className="main-container">
      <TestButton />

      {/* 
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

export default MainContainer;
