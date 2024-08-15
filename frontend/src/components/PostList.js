import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import PostService from '../services/PostService';
import { Card, CardContent, Typography, CardMedia } from '@mui/material';
import EventIcon from '@mui/icons-material/Event';
import PersonIcon from '@mui/icons-material/Person';
import CategoryIcon from '@mui/icons-material/Category';
import './PostList.css';  // Import the CSS file

const PostList = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    PostService.getPosts().then((response) => {
      setPosts(response.data);
    });
  }, []);

  return (
    <div>
      <div className="banner">
        <div className="banner-overlay"></div> {/* Overlay for the banner */}
        <div className="banner-text">
          Your Guide to Lebanon's Hidden Secrets
        </div>
      </div>
      <div className="post-list-container">
        <div className="post-list-grid">
          {posts.map((post) => (
            <Card className="post-card" key={post.id}>
              {post.featured_image && (
                <CardMedia
                  component="img"
                  className="post-card-media"
                  image={post.featured_image}
                  alt={post.title}
                />
              )}
              <CardContent className="post-card-content">
                <Typography
                  variant="h6"
                  component={Link}
                  to={`/blog/post/${post.id}`}
                  className="post-card-title"
                >
                  {post.title}
                </Typography>
                <div className='meta-data'>
                <div className="post-meta">
                  <EventIcon className="post-meta-icon" />
                  {new Date(post.updated_at).toLocaleDateString()}
                </div>
                <div className="post-meta">
                  <PersonIcon className="post-meta-icon" />
                  {post.author}
                </div>
                <div className="post-meta">
                  <CategoryIcon className="post-meta-icon" />
                  {post.category ? post.category.name : 'Uncategorized'}
                </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PostList;
