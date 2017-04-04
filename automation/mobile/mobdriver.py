#!/usr/bin/env python

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from appium import webdriver
from selenium.webdriver.common.by import By

from automation.mobile.platforms import Platform
from automation.mobile.uicomponents import UIComponents

import os

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class MobDriver(webdriver.Remote):

    def __init__(self, command_executor='http://127.0.0.1:4444/wd/hub',
                 desired_capabilities=None, browser_profile=None, proxy=None, keep_alive=False):
        super(MobDriver, self).__init__(command_executor, desired_capabilities, browser_profile, proxy,
                                        keep_alive)
        # get copy of desired_capabilities dict
        self.desired_caps = desired_capabilities
        # identify platform
        if self.desired_caps['platformName'] == "Android":
            self.platform = Platform.ANDROID
        elif self.desired_caps['platformName'] == "iOS":
            self.platform = Platform.IOS
        else:
            self.platform = Platform.UNKNOWN

    def find(self, widget_type: UIComponents, name: str):
        """ 
        :param name: Name of the component
        :param widget_type: Type of widget UIComponents
        :return: returns labeled element of type 
        """

        if self.platform == Platform.IOS:
            lookup_xpath = widget_type.iOS.format("@hint='{0}' or @value={0} or @label={0} or @name={0}")
        elif self.platform == Platform.ANDROID:
            lookup_xpath = widget_type.Android.format("@text='{0}'")

        lookup_xpath = lookup_xpath.format(name)
        return self.find_element_by_xpath(lookup_xpath)

    def find(self, widget_type: UIComponents, index: int):
        """
        :param index: Index of component to return from list
        :param widget_type: Type of widget UIComponents
        :return: returns labeled element of type
        """

        if self.platform == Platform.IOS:
            lookup_xpath = widget_type.iOS
        elif self.platform == Platform.ANDROID:
            lookup_xpath = widget_type.Android

        return self.find_element_by_xpath(lookup_xpath.format(index))