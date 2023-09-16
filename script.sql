-- phpMyAdmin SQL Dump
-- version 4.4.15.10
-- https://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: 2023-09-15 17:34:55
-- 服务器版本： 5.6.50-log
-- PHP Version: 5.6.40

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hexo_view`
--

-- --------------------------------------------------------

--
-- 表的结构 `hv_article`
--

CREATE TABLE IF NOT EXISTS `hv_article` (
  `id` int(11) NOT NULL,
  `address` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- 表的结构 `hv_user`
--

CREATE TABLE IF NOT EXISTS `hv_user` (
  `ip` varchar(60) NOT NULL,
  `id` int(11) NOT NULL,
  `view1` int(11) NOT NULL DEFAULT '0',
  `view2` int(11) NOT NULL DEFAULT '0',
  `view3` int(11) NOT NULL DEFAULT '0',
  `view4` int(11) NOT NULL DEFAULT '0',
  `view5` int(11) NOT NULL DEFAULT '0',
  `view6` int(11) NOT NULL DEFAULT '0',
  `view7` int(11) NOT NULL DEFAULT '0',
  `view8` int(11) NOT NULL DEFAULT '0',
  `view9` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `hv_article`
--
ALTER TABLE `hv_article`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `hv_article`
--
ALTER TABLE `hv_article`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
