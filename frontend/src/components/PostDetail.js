import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Typography, Container, Box } from '@mui/material';
import PostService from '../services/PostService';
import './PostDetail.css';  // Import the CSS file

const PostDetail = () => {
  const { id } = useParams();
  const [post, setPost] = useState(null);

  useEffect(() => {
    PostService.getPost(id).then((response) => {
      setPost(response.data);
    });
  }, [id]);

  if (!post) return <div>Loading...</div>;

  return (
    <Container maxWidth="md" className="post-detail-container">
      <Box mt={4}>
        <Typography variant="h3" component="h1" gutterBottom className="post-detail-title">
          {post.title}
        </Typography>
        {post.featured_image && (
          <img
            src={post.featured_image}
            alt={post.title}
            className="post-detail-featured-image"
          />
        )}
        <Typography variant="body1" component="div" gutterBottom className="post-detail-content">
          <div dangerouslySetInnerHTML={{ __html: post.content }} />
        </Typography>
        <Typography variant="body2" color="textSecondary" gutterBottom className="post-detail-meta">
          Updated on: {new Date(post.updated_at).toLocaleDateString()} by {post.author}
        </Typography>
        <Typography variant="body2" color="textSecondary" className="post-detail-meta">
          Category: {post.category ? post.category.name : 'Uncategorized'}
        </Typography>
      </Box>
    </Container>
  );
};

export default PostDetail;
